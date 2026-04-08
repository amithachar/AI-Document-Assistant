import os
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import chromadb

# 🔐 Login to HuggingFace (uses env variable HF_TOKEN)
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=os.getenv("HF_TOKEN"))

# ⚡ Use smaller model for speed
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# 📦 Load tokenizer & model
print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32   # ✅ fixed warning
)

model = model.to("cpu")

print("Model loaded successfully!")

# 🧠 ChromaDB setup
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="rag_collection")


# 🔍 Retrieve context
def retrieve_context(query, k=3):
    try:
        results = collection.query(query_texts=[query], n_results=k)

        # ✅ check if results exist
        if not results or "documents" not in results:
            return "No context found"

        docs = results["documents"][0]

        # ✅ check if empty
        if not docs:
            return "No context available"

        return "\n".join(docs)

    except Exception as e:
        print("CHROMA ERROR:", e)
        return "No context"


# 🤖 Generate answer
def generate_answer(query):
    try:
        context = retrieve_context(query)

        prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{query}

Answer:
"""

        inputs = tokenizer(prompt, return_tensors="pt")

        # 🔥 add no_grad (VERY IMPORTANT for speed)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,   # reduce more
                temperature=0.7
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response

    except Exception as e:
        print("ERROR IN GENERATE:", e)
        return f"Error: {str(e)}"