from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.rag import generate_answer
from app.ingest import ingest_documents

app = FastAPI()


# ✅ Request model
class QueryRequest(BaseModel):
    query: str


# ✅ Ask endpoint (already exists)
@app.post("/ask")
def ask_question(request: QueryRequest):
    return {"answer": generate_answer(request.query)}


# ✅ ADD THIS → Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = content.decode("utf-8", errors="ignore")
    except:
        text = str(content)

    ingest_documents([text])

    return {"message": "Document uploaded successfully"}    

@app.get("/")
def root():
    return {"message": "API is running"}