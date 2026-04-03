import chromadb
import requests
import os
from app.embedder import get_embeddings

# Initialize ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection(name="rag_docs")

# Ollama URL (local or k8s)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

# Add documents
def add_documents(docs):
    embeddings = get_embeddings(docs)

    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc],
            embeddings=[embeddings[i]],
            ids=[f"id_{i}_{hash(doc)}"]
        )

# RAG function
def ask_rag(query: str):
    try:
        # Step 1: Embed query
        query_embedding = get_embeddings([query])[0]

        # Step 2: Retrieve context
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        context = " ".join(results["documents"][0])

        # Step 3: Prompt
        prompt = f"""
You are a highly intelligent AI assistant.

Answer the question in a detailed and structured way.

Context:
{context}

Question:
{query}

Instructions:
- Give a detailed explanation
- Use bullet points if helpful
- Do not give short answers
"""

        # Step 4: Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            },
            timeout=60
        )

        print("OLLAMA RESPONSE:", response.text)  # debug

        try:
            return response.json().get("response", "No response")
        except:
            return f"Invalid JSON from Ollama: {response.text}"

    except Exception as e:
        return f"Error in RAG pipeline: {str(e)}"