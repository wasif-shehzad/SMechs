import streamlit as st
import requests

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# 2025 Standard Configuration
st.set_page_config(page_title="SMechs RAG Assistant", page_icon="🤖")
st.title("🤖 SMechs Document AI")

# Backend Configuration
FASTAPI_URL = "http://localhost:8000"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for PDF Uploads
with st.sidebar:
    st.header("Document Management")
    uploaded_file = st.file_uploader("Upload PDF to Knowledge Base", type="pdf")
    category = st.text_input("Category/Namespace", value="general")
    
    if st.button("Upload & Index"):
        if uploaded_file and category:
            with st.spinner("Processing PDF..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                # Updated to match your 'add' endpoint from previous steps
                response = requests.post(f"{FASTAPI_URL}/api/v1/documents/?category={category}", files=files)
                if response.status_code == 201:
                    st.success("Document indexed in Pinecone!")
                else:
                    st.error(f"Upload failed: {response.text}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # updated payload to match your chat endpoint
                payload = {"query": prompt, "category": category}
                response = requests.post(f"{FASTAPI_URL}/api/v1/documents/chat", json=payload)
                
                if response.status_code == 200:
                    full_response = response.json()
                    message = None
                    for msg in full_response["messages"]:
                        print("Message received:", msg)
                        if msg["type"] == "ai" and msg["content"]:
                            message = msg["content"]

                    st.markdown(message)
                    st.session_state.messages.append({"role": "assistant", "content": message})
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
