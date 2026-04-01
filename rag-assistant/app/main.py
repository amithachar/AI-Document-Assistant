from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.ingest import process_document
from app.rag import ask_rag

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "RAG Assistant Running 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    
    try:
        text = content.decode("utf-8")
    except:
        text = str(content)  # fallback for PDF (temporary)

    process_document(content)
    return {"message": "Document uploaded"}

@app.post("/ask")
def ask(req: QueryRequest):
    return {"response": ask_rag(req.query)}