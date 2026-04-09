from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

CHROMA_PATH = "/data/chroma"

def get_retriever():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )

    return db.as_retriever(search_kwargs={"k": 3})  # 🔥 limit here also