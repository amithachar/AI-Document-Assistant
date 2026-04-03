import streamlit as st
import requests
import time

# Page config
st.set_page_config(page_title="PrivateGPT", page_icon="🤖", layout="centered")

# Custom CSS (Gradient + styling)
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-box {
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
}

.user-msg {
    background-color: #1f2937;
    color: white;
    text-align: right;
}

.bot-msg {
    background-color: #374151;
    color: white;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🤖 PrivateGPT</div>', unsafe_allow_html=True)
st.write("### Your Local AI Document Assistant")

# Check backend
try:
    requests.get("http://localhost:8000")
except:
    st.error("❌ FastAPI not running")
    st.stop()

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload section
with st.expander("📂 Upload Document"):
    uploaded_file = st.file_uploader("Upload TXT or PDF")

    if uploaded_file:
        with st.spinner("Processing document..."):
            files = {"file": ("file", uploaded_file.getvalue())}
            requests.post("http://localhost:8000/upload", files=files)
        st.success("✅ Document uploaded successfully")

# Chat input
query = st.chat_input("Ask something about your document...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message
    st.markdown(f'<div class="chat-box user-msg">{query}</div>', unsafe_allow_html=True)

    # Call backend
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:8000/ask",
            json={"query": query}
        )

    try:
       if response.status_code == 200:
        data = response.json()
        answer = data.get("response", "No response")
       else:
        answer = f"❌ API Error: {response.text}"
    except Exception as e:
       answer = f"❌ Invalid response from server:\n{response.text}"

    # Smooth typing effect
    placeholder = st.empty()
    full_text = ""

    for word in answer.split():
        full_text += word + " "
        placeholder.markdown(
            f'<div class="chat-box bot-msg">{full_text}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.02)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Show chat history (persistent)
st.write("---")
st.write("### 💬 Chat History")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-box user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-box bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)