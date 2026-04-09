import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.title("📄 AI Document Assistant")

token = st.text_input("Enter API Token", type="password")
query = st.text_area("Ask a question")

if st.button("Ask"):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.post(
        API_URL,
        json={"query": query},
        headers=headers
    )

    if res.status_code == 200:
        st.write(res.json()["answer"])
    else:
        st.error(res.text)