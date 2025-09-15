from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from typing import Iterable
import os

local_model_path = "model/all-MiniLM-L6-v2"



def initialize_vector_db(documents: Iterable[Document], persist_dir: str = None) -> Chroma:
    persist_dir = persist_dir or os.getenv("LOCAL_PERSIST_PATH", './vectorstore/')
    embeddings = HuggingFaceEmbeddings(model_name=local_model_path)
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    return vector_db

def load_vector_db(persist_dir: str = "./vectorstore") -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=local_model_path)
    vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vector_db