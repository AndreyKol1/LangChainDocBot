from typing import TypedDict, List, Annotated
from langchain_core.documents import Document
from langgraph.graph import add_messages

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    documents_reranked: list
    messages: Annotated[list, add_messages]

    