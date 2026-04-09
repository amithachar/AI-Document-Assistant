from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import rag_pipeline
from app.embedder import get_retriever

app = FastAPI()

# 🔥 LOAD ONCE (IMPORTANT)
retriever = get_retriever()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_api(req: QueryRequest):
    response = rag_pipeline(req.query, retriever)
    return {"answer": response}