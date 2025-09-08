from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from typing import Iterable

def initialize_vector_db(documents: Iterable[Document], persist_dir: str = 'data/vectorstore/') -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    return vector_db

def load_vector_db(persist_dir: str) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vector_db