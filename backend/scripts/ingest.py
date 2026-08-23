from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

from app.config import get_settings
from content.knowledge import CHUNKS

settings = get_settings()

pc = Pinecone(api_key=settings.pinecone_api_key)
embedder = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)

EMBEDDING_DIMENSION = 1536

if settings.pinecone_index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=settings.pinecone_index_name,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(settings.pinecone_index_name)

index.delete(delete_all=True)
print("Cleared existing vectors from index.")

texts = [chunk["text"] for chunk in CHUNKS]
vectors = embedder.embed_documents(texts)

records = [
    {
        "id": f"chunk-{i}",
        "values": vector,
        "metadata": {"category": chunk["category"], "text": chunk["text"]},
    }
    for i, (chunk, vector) in enumerate(zip(CHUNKS, vectors))
]

index.upsert(vectors=records)

print(f"Upserted {len(records)} chunks into index '{settings.pinecone_index_name}'.")
