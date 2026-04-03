from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag import add_documents
from pypdf import PdfReader
import io

def process_document(file_bytes):
    text = ""

    # Try TXT
    try:
        text = file_bytes.decode("utf-8")
    except:
        # Handle PDF
        pdf = PdfReader(io.BytesIO(file_bytes))
        for page in pdf.pages:
            text += page.extract_text() or ""

    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    # Store in vector DB
    add_documents(chunks)

    return chunks