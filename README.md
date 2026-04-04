# AI-Document-Assistant
AI-Document-Assistant built on python base 

It's a local AI document assistant — think of it like a private ChatGPT that only knows what's in your own documents.
Here's the simple idea: you upload your PDFs or text files, and then you can ask questions about them in plain English. The app finds the relevant parts of your documents and uses a local LLM (running on your own machine/server via Ollama) to generate an answer — no data ever leaves your infrastructure.
The three things it does:

1.Ingests your docs — reads PDFs/text, splits them into chunks, converts each chunk into a vector (a list of numbers that captures meaning), and stores them in ChromaDB.

2.Understands your questions — when you ask something, it converts your question into the same kind of vector and finds the most semantically similar chunks from your documents.

3.Generates an answer — stuffs those relevant chunks as context into a prompt and sends it to a local Llama 3 model, which writes a coherent answer grounded in your actual documents.

A practical example: upload your company's 200-page policy manual, then ask "what is the leave policy for contractors?" — it finds the right section and answers directly, without you having to search manually.
The "local" and "Kubernetes" parts mean it runs entirely on your own servers, scales horizontally, and your sensitive documents never touch OpenAI or any external API.


# 📁 Project Structure Overview
```
rag-assistant/
│
├── app/
│   ├── main.py        # API entry point
│   ├── ingest.py      # Load + chunk documents
│   ├── embedder.py    # Convert text → vectors
│   └── rag.py         # Retrieval + LLM response
│
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container build
│
└── k8s/
    ├── fastapi-deployment.yaml
    ├── chromadb-deployment.yaml
    ├── ollama-deployment.yaml
    └── pvc.yaml
```

# 🔄 Step-by-Step How the App Works

## 1️⃣ Document Ingestion (ingest.py)

👉 Purpose: Prepare your knowledge base
  
  What happens:
  Load documents (PDF, TXT, etc.)
  Split into chunks (small pieces)
  Send chunks for embedding
  Example flow:
  docs → split → ["chunk1", "chunk2", ...]


## 2️⃣ Embedding Generation (embedder.py)

👉 Purpose: Convert text → vector (numerical representation)

Why?

Machines can't understand text directly, so we convert it into vectors.

Example:
"DevOps is important" → [0.23, 0.91, 0.11, ...]
Output:
Each chunk gets a vector
Stored in vector DB (ChromaDB)

## 3️⃣ Vector Storage (ChromaDB - via k8s)

👉 Your chromadb-deployment.yaml runs:

Vector database
Stores:
chunk text
embeddings
Example:
{
  "text": "Kubernetes is...",
  "embedding": [0.12, 0.88, ...]
}

## 4️⃣ API Layer (main.py - FastAPI)

👉 This is your entry point

Example endpoint:
POST /ask
{
  "question": "What is Kubernetes?"
}
What it does:
Receives user question
Calls rag.py

## 5️⃣ RAG Logic (rag.py)

👉 Core brain of the system

Steps:
🔍 Step 1: Embed the query
"What is Kubernetes?" → vector
🔎 Step 2: Search similar chunks
Query ChromaDB
Find top relevant chunks
🧾 Step 3: Build context
Context:
"Kubernetes is a container orchestration tool..."
🤖 Step 4: Send to LLM (Ollama)
Combine:
user question
retrieved context

Prompt example:

Answer using this context:
[retrieved chunks]

Question:
What is Kubernetes?

##6️⃣ LLM (Ollama Deployment)

👉 Your ollama-deployment.yaml runs:

Local LLM (like Llama3, Mistral)
It:
Receives prompt
Generates final answer
7️⃣ Response Back to User
LLM → rag.py → main.py → User
🐳 Dockerfile

👉 Packages your app into a container

Includes:

Python
Dependencies
FastAPI app

Used in:
Kubernetes deployment

## ☸️ Kubernetes (k8s folder)

You are running a microservices architecture:

1. fastapi-deployment.yaml
Runs your API (main.py)
2. chromadb-deployment.yaml
Runs vector database
3. ollama-deployment.yaml
Runs LLM
4. pvc.yaml
Persistent storage
Keeps embeddings safe

## 🔄 Complete Flow Diagram

        ┌──────────────┐
        │   User       │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ FastAPI      │ (main.py)
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   RAG Logic  │ (rag.py)
        └──────┬───────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ ChromaDB     │  │ Ollama (LLM) │
│ (vector DB)  │  │              │
└──────────────┘  └──────────────┘
      ▲
      │
┌──────────────┐
│ ingest.py    │
└──────────────┘

🧠 Simple Real-World Analogy

Think of it like:

📚 ingest.py → Creates your personal notes
🧠 embedder.py → Indexes your notes
🔍 rag.py → Finds best notes for question
🤖 Ollama → Explains answer nicely
🌐 main.py → Acts like receptionist
🔥 Why This Architecture Is Powerful
✅ Uses your own data
✅ No hallucination (context grounded)
✅ Fully local (Ollama)
✅ Scalable (Kubernetes)
✅ Production-ready
🚀 If You Want Next Step

I can help you with:

✅ Full working code for each file
✅ Kubernetes YAML (production-ready)
✅ CI/CD pipeline (Jenkins/GitHub Actions)
✅ Monitoring (Prometheus + Grafana)



