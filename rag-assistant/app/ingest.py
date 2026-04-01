from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag import add_documents
from pypdf import PdfReader
import io

def process_document(file_bytes):
    try:
        text = file_bytes.decode("utf-8")
    except:
        # PDF handling
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)
    add_documents(chunks)

    return chunks