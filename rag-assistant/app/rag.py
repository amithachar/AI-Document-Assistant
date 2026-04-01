import chromadb
import requests
from app.embedder import get_embeddings

# Initialize ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection(name="rag_docs")

# Add documents
def add_documents(docs):
    embeddings = get_embeddings(docs)

    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc],
            embeddings=[embeddings[i]],
            ids=[f"id_{i}"]
        )

# Query + LLM
def ask_rag(query: str):
    query_embedding = get_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = " ".join(results["documents"][0])

    prompt = f"""
You are an AI assistant. Answer based only on the context.

Context:
{context}

Question:
{query}
"""

    # ⚠️ Change URL depending on environment
    OLLAMA_URL = "http://localhost:11434/api/generate"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json().get("response", "No response")