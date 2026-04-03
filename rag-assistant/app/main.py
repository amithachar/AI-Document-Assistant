from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.ingest import process_document
from app.rag import ask_rag

app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "RAG Assistant Running 🚀"}

# Upload document (TXT / PDF)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    process_document(content)
    return {"message": "Document processed successfully"}

# Ask question
@app.post("/ask")
def ask(req: QueryRequest):
    return {"response": ask_rag(req.query)}