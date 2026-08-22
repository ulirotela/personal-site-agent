from app.agent import ProductionAgent

agent = ProductionAgent()

queries = [
    'Does uli have any siblings?',
    'what are the siblings name?',
]

for query in queries:
    print(f'Question: {query}')
    result = agent.invoke(query)
    print(f'Response: {result["response"][:150]}')
    print(f'Model:    {result["model_used"]}')
    print(f'Error:    {result["error"]}')
    print()