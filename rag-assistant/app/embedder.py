import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-service:11434/api/embeddings")

def get_embeddings(texts):
    embeddings = []
    for text in texts:
        res = requests.post(
            OLLAMA_URL,
            json={"model": "mistral", "prompt": text}
        )
        embeddings.append(res.json()["embedding"])
    return embeddings