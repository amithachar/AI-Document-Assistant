import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "qwen:7b"   # or qwen2:1.5b (faster)

def build_prompt(context, query):
    return f"""
You are a helpful assistant.

Answer ONLY using the context below.
If answer is not in context, say "I don't know".

Context:
{context}

Question:
{query}
"""


def call_qwen(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    return response.json()["response"]


def rag_pipeline(query, retriever):
    # 🔥 LIMIT DOCUMENTS (critical fix)
    docs = retriever.get_relevant_documents(query)
    docs = docs[:3]

    # 🔥 TRIM CONTEXT (critical fix)
    context = "\n\n".join([d.page_content for d in docs])
    context = context[:2000]

    prompt = build_prompt(context, query)

    return call_qwen(prompt)