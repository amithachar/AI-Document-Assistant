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
