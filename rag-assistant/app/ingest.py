import chromadb
from app.embedder import get_embedding

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="rag_collection")


def ingest_documents(docs):
    for i, doc in enumerate(docs):
        embedding = get_embedding(doc)
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )