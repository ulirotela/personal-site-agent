"""
Knowledge base content for RAG.
Each entry is a self-contained chunk (one idea per chunk) tagged with the
category it belongs to — matches the routing categories in app/agent.py
(experience / projects / contact), so retrieval can filter by category
when we wire this into Pinecone (Step 6).
"""

CHUNKS = [
    # --- Profile / experience ---
    {
        "category": "experience",
        "text": (
            "Uli Rotela is an AI Engineer based in Dublin, Ireland, with 9+ years of combined "
            "experience in IT operations, infrastructure management, and technical support across "
            "international environments, now applying that operational rigor to building "
            "production-grade AI systems. He combines a strong service and reliability mindset with "
            "a software development background and hands-on experience in Python, FastAPI, "
            "LangGraph, RAG pipelines, and multi-agent architectures."
        ),
    },
    {
        "category": "experience",
        "text": (
            "From March 2023 to March 2026, Uli worked as a Systems Engineer at General Motors IT "
            "Services Ireland, supporting IT and AV infrastructure across 9 live Experience Centers "
            "in 5 European countries. He was the sole technical owner for AV and conferencing systems "
            "(Cisco video conferencing, Biamp DSPs, Lightware video matrix, Pixera media servers), "
            "administered network infrastructure via Cisco Meraki, and built automation scripts and "
            "API integrations to reduce manual operational work across sites."
        ),
    },
    {
        "category": "experience",
        "text": (
            "Before General Motors, Uli worked as a Technical Support Engineer at Cibersons Group "
            "(2016-2020), providing remote helpdesk support to B2B clients across hardware, software, "
            "and network issues, managing servers and workstations, and resolving escalated technical "
            "issues with product and engineering teams."
        ),
    },
    {
        "category": "experience",
        "text": (
            "Uli holds an MSc in Applied Software Development (QQI Level 9) from CCT College Dublin "
            "(2nd Class Honours), an MSc in Development Practice (QQI Level 9) from Trinity College "
            "Dublin, and a Bachelor's degree in Computer Science from the Catholic University of "
            "Asuncion, Paraguay."
        ),
    },
    {
        "category": "experience",
        "text": (
            "Uli's technical skill set spans both IT operations and AI engineering: Python, FastAPI, "
            "LangChain, LangGraph, RAG pipelines with Pinecone and ChromaDB, multi-agent "
            "orchestration, Docker, Git, and pytest, plus deep systems experience with macOS/Windows/"
            "Linux administration, networking (TCP/IP, DNS, DHCP, Cisco Meraki), and SaaS platform "
            "administration (Google Workspace, Microsoft 365, Slack, Atlassian)."
        ),
    },
    # --- Projects ---
    {
        "category": "projects",
        "text": (
            "Uli built a production-grade chat API using FastAPI and LangGraph, featuring a security "
            "pipeline (input sanitization, PII detection, output validation), response caching with "
            "TTL, automatic retry and fallback between OpenAI and Anthropic models, structured "
            "logging, metrics collection, and LangSmith tracing. It's fully tested with pytest, "
            "containerized with Docker, and deployed on Render."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli's personal website runs on a multi-agent system built with LangGraph: a "
            "classification agent routes each visitor question to one of three specialist agents "
            "(experience, projects, or contact), each retrieving relevant content through a RAG "
            "pipeline backed by Pinecone. The system includes automatic fallback from OpenAI to "
            "Anthropic models for reliability, and is fully containerized and deployed."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli delivered a freelance project for VEMSA Consultora, an accounting firm in Paraguay: "
            "a full public website, a client portal with document and case management, and an "
            "internal admin panel for staff — all designed and iterated based on direct client "
            "feedback and real brand research."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli built Interviewer Pro, an AI-powered mock interview simulator using Streamlit and "
            "GPT-4o, which conducts a structured practice interview based on the user's target role "
            "and company, then generates a score and detailed feedback."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli built a computer vision system for automated broken screen detection, rebuilding "
            "and extending a solution he originally worked on while supporting device fleets at "
            "General Motors. The system uses a trained vision model served through a FastAPI "
            "endpoint to classify device screen images as damaged or intact."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli built a multi-tenant SaaS chatbot platform that lets businesses deploy an AI "
            "assistant connected to WhatsApp Business for sales and customer support. It uses "
            "isolated per-client configuration and knowledge bases on top of the same reusable "
            "LangGraph engine, with authentication and usage isolation between tenants."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli built an evaluation and observability framework for his AI agents: a test dataset "
            "of representative questions paired with automated metrics for accuracy, hallucination "
            "detection, latency, and cost per response — giving visibility into how his production "
            "systems perform beyond just 'it works'."
        ),
    },
    {
        "category": "projects",
        "text": (
            "Uli built a website with an embedded AI assistant for the Paraguayan community in "
            "Ireland, reusing the same multi-tenant chatbot engine with content and configuration "
            "tailored to that community, deployed end-to-end for real users."
        ),
    },
    # --- Personal ---
    {
        "category": "personal",
        "text": (
            "Uli is originally from Paraguay and now lives in Dublin, Ireland, he has been 10 years in Ireland. He has three "
            "brothers, Orlando, Alan and Victor, all of them men, making him one of four siblings. Outside of engineering, "
            "he enjoys cycling and building with Lego sets."
        ),
    },
    {
        "category": "personal",
        "text": (
            "Uli is a big science fiction fan. Some of his favorite sci-fi movies include Alien, "
            "Predator, Blade Runner, Blade Runner 2049, Matrix, Terminator, Terminator 2: "
            "Judgment Day, Star Wars: A New Hope, Interstellar, Arrival, Dune, Dune: Part Two, 2001: "
            "A Space Odyssey, Ex Machina, District 9, Edge of Tomorrow, Inception, Minority Report, "
            "The Thing, and Children of Men. He also enjoys reading science fiction novels, "
            "including Dune by Frank Herbert, Neuromancer by William Gibson, The Three-Body Problem "
            "by Liu Cixin, Ender's Game by Orson Scott Card, and Foundation by Isaac Asimov."
        ),
    },
    # --- Contact ---
    {
        "category": "contact",
        "text": (
            "Uli is based in Dublin, Ireland, holds a Stamp 4 visa with full working rights (no "
            "sponsorship required), and is fluent in English and a native Spanish speaker. "
            "Email: ulirotela@gmail.com. GitHub: github.com/ulirotela."
        ),
    },
]
