import streamlit as st
import requests

st.title("📄 RAG AI Assistant")

# Check backend
try:
    requests.get("http://localhost:8000")
    st.success("✅ FastAPI Connected")
except:
    st.error("❌ FastAPI not running")
    st.stop()

# Upload file
uploaded_file = st.file_uploader("Upload document")

if uploaded_file:
    files = {"file": ("file.txt", uploaded_file.getvalue())}
    res = requests.post("http://localhost:8000/upload", files=files)
    st.success("✅ Document uploaded")

# Ask question
query = st.text_input("Ask a question")

if st.button("Ask"):
    if not query.strip():
        st.warning("⚠️ Enter a question")
    else:
        res = requests.post(
            "http://localhost:8000/ask",
            json={"query": query}
        )

        if res.status_code == 200:
            st.write("🤖 Answer:")
            st.write(res.json()["response"])
        else:
            st.error(res.text)