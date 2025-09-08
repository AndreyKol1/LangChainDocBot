from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os 

load_dotenv()
api_key = os.environ["GROQ_API_KEY"]

def initialize_model():
    llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
)
    return llm