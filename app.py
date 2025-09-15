import streamlit as st
from streamlit_chat import message  
from utils.gcp import download_directory_from_gcs
import os

BUCKET_NAME = os.getenv("BUCKET_NAME", "chromavecdb17")
GCS_PERSIST_PATH = os.getenv("GCS_PERSIST_PATH", "chroma/")
LOCAL_PERSIST_PATH = os.getenv("LOCAL_PERSIST_PATH", "./vectorstore")

download_directory_from_gcs(GCS_PERSIST_PATH, LOCAL_PERSIST_PATH, BUCKET_NAME)

from src.main import ask_question

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTitle { color: #4CAF50; font-family: 'Arial', sans-serif; }
    .stChatInput { border-radius: 10px; }
    .stMarkdown { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)


st.title("🤖 LangChain Documentation Chatbot")
st.markdown("Ask me anything about LangChain documentation!")


if "messages" not in st.session_state:
    st.session_state.messages = []


for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")
    else:
        message(msg["content"], is_user=False, key=f"assistant_{i}")


if prompt := st.chat_input("What you would like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    message(prompt, is_user=True)
    print(prompt)
    

    with st.spinner("Thinking..."):
        try:
            response = ask_question(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            message(response, is_user=False)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            response = "Sorry, I couldn't process that."
            st.session_state.messages.append({"role": "assistant", "content": response})
            message(response, is_user=False)