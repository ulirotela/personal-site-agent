"""
LangGraph Agent with Production Error Handling
Retry logic, model fallback, and structured state management.
"""

from typing import Optional
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langsmith import traceable
from pydantic import BaseModel
from typing import Literal
from langchain_core.messages import SystemMessage
from pinecone import Pinecone as PineconeClient
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from app.config import get_settings


# === Agent State ===

class AgentState(TypedDict):
    """
    State for the production agent.
    Uses Annotated with add_messages reducer for message accumulation.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    error: Optional[str]
    model_used: str
    route: str

class Intent(BaseModel):
    category: Literal["experience", "projects", "contact", "personal"]

# === Agent Builder ===

class ProductionAgent:
    """
    Production LangGraph agent with:
    - Retry on failure (model fallback)
    - Graceful error handling
    - LangSmith tracing
    """

    def __init__(self):
        settings = get_settings()

        self.primary_llm = ChatOpenAI(
            model=settings.primary_model,
            temperature=0,
            timeout=30,
            max_retries=0,  # We handle retries ourselves
            api_key=settings.openai_api_key,
        )
        self.fallback_llm = ChatAnthropic(
            model=settings.fallback_model,
            temperature=0,
            timeout=30,
            max_retries=0,
            api_key=settings.anthropic_api_key,
        )
        self.pc = PineconeClient(api_key=settings.pinecone_api_key)
        self.pinecone_index = self.pc.Index(settings.pinecone_index_name)
        self.embedder = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)
        self.pool = ConnectionPool(
            conninfo=settings.database_url,
            max_size=20,
            kwargs={"autocommit": True, "prepare_threshold": 0},
        )
        self.checkpointer = PostgresSaver(self.pool)
        self.checkpointer.setup()

        with self.pool.connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_activity (
                    thread_id TEXT PRIMARY KEY,
                    last_seen TIMESTAMPTZ NOT NULL DEFAULT now()
                )
            """)

        self.graph = self._build_graph()

    def _invoke_with_fallback(self, messages: list)-> dict:
        """Shared reliability layer: try primary model, fall back to secondary, else graceful error."""
        try:
            response = self.primary_llm.invoke(messages)
            return {"messages": [response], "error": None, "model_used":"primary"}
        except Exception:
            try:
                response = self.fallback_llm.invoke(messages)
                return {"messages": [response], "error": None, "model_used":"fallback"}
            except Exception as e:
                return {
                    "messages": [AIMessage(content="Sorry, I'm having trouble right now. Please try again in a moment.")],
                    "error": str(e),
                    "model_used": "error",
            }

    def _retrieve_context(self, query: str, category: str, top_k: int = 3) -> str:
        """Retrieve the most relevant knowledge chunks for this query, filtered by category."""
        query_vector = self.embedder.embed_query(query)
        results = self.pinecone_index.query(
            vector=query_vector,
            top_k=top_k,
            filter={"category": {"$eq": category}},
            include_metadata=True,
        )
        chunks = [match["metadata"]["text"] for match in results["matches"]]
        return "\n\n".join(chunks)

    def _build_graph(self):
        """Build the LangGraph state machine."""

        def classify_intent(state: AgentState) -> dict:
            system_prompt = SystemMessage(content="""
            You classify visitor questions on Uli's site into one of these categories:
            - experience: about his work history, skills, CV, professional experience.
            - projects: about specific technical projects (VEMSA, Production API, Broken Screen Detection), architecture, or stack.
            - contact: wants to contact him, schedule a call, or asks about availability.
            - personal: about hobbies, interests, or what Uli likes outside of work.
            Choose the category that best matches the latest question.
            """)
            last_message = state["messages"][-1]
            try:
                classifier = self.primary_llm.with_structured_output(Intent)
                result = classifier.invoke([system_prompt, last_message])
                return {"route": result.category}
            except Exception:
                try:
                    classifier = self.fallback_llm.with_structured_output(Intent)
                    result = classifier.invoke([system_prompt, last_message])
                    return {"route": result.category}
                except Exception as e:
                    return {
                        "route": "error",
                        "messages": [AIMessage(content="Sorry, I'm having trouble right now. Please try again in a moment.")],
                        "error": str(e),
                        "model_used": "error",
                    }
        
        def route_by_intent(state: AgentState)-> str:
            return state["route"]

        def answer_experience(state: AgentState) -> dict:
            last_message = state["messages"][-1]
            context = self._retrieve_context(last_message.content, category="experience")
            system_prompt = SystemMessage(content=f"""
            You are Uli Rotela's assistant. Answer questions about his work experience, skills, and CV
            using this info:

            {context}

            Keep answers concise, professional, and specific — cite real projects when relevant.
            """)
            return self._invoke_with_fallback([system_prompt] + state["messages"])

        def answer_project(state: AgentState)-> dict:
            last_message = state["messages"][-1]
            context = self._retrieve_context(last_message.content, category="projects")
            system_prompt = SystemMessage(content=f"""
            You are Uli Rotela's assistant. Answer questions about his technical projects, architecture,
            and stack using this info:

            {context}

            Keep answers concise and technical — mention real architecture choices when asked.
            """)
            return self._invoke_with_fallback([system_prompt] + state["messages"])


        def answer_contact(state: AgentState)-> dict:
            last_message = state["messages"][-1]
            context = self._retrieve_context(last_message.content, category="contact")
            system_prompt = SystemMessage(content=f"""
            You are Uli Rotela's assistant. Help visitors get in touch with him using this info:

            {context}

            If someone wants to reach out, hire him, or schedule a call: confirm what they're interested in
            (a role, a freelance project, a general question), then point them to the contact info above.
            Keep it short, friendly, and professional.
            """)
            return self._invoke_with_fallback([system_prompt] + state["messages"])

        def answer_personal(state: AgentState) -> dict:
            last_message = state["messages"][-1]
            context = self._retrieve_context(last_message.content, category="personal")
            system_prompt = SystemMessage(content=f"""
            You are Uli Rotela's assistant. Answer questions about his hobbies and interests outside of work
            using this info:

            {context}

            Keep answers light, friendly, and brief.
            """)
            return self._invoke_with_fallback([system_prompt] + state["messages"])

        # Build the graph
        graph = StateGraph(AgentState)

        graph.add_node("classify", classify_intent)
        graph.add_node("experience", answer_experience)
        graph.add_node("project", answer_project)
        graph.add_node("contact", answer_contact)
        graph.add_node("personal", answer_personal)

        graph.add_edge(START, "classify")

        graph.add_conditional_edges(
            "classify",
            route_by_intent,
            {"experience":"experience", "projects": "project", "contact": "contact", "personal": "personal", "error": END },
        )

        graph.add_edge("experience", END)
        graph.add_edge("project", END)
        graph.add_edge("contact", END)
        graph.add_edge("personal", END)

        return graph.compile(checkpointer=self.checkpointer)

    @traceable(name="production_agent_invoke")
    def invoke(self, message: str, thread_id: str) -> dict:
        """
        Invoke the agent with a user message.
        Returns: {"response": str, "model_used": str, "error": str | None}
        """

        result = self.graph.invoke(
            {
                "messages": [HumanMessage(content=message)],
                "error": None,
                "model_used": "",
            },
            config={"configurable": {"thread_id": thread_id}},
        )

        with self.pool.connection() as conn:
            conn.execute(
                """
                INSERT INTO conversation_activity (thread_id, last_seen)
                VALUES (%s, now())
                ON CONFLICT (thread_id) DO UPDATE SET last_seen = now()
                """,
                (thread_id,),
            )

        return {
        "response": result["messages"][-1].content,
        "model_used": result.get("model_used", "unknown"),
        "error": result.get("error"),
        }