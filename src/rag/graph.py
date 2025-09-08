# from backend.app.rag.prompt import create_chat_prompt
# from backend.app.rag.generator_ import initialize_model
# from scripts.ingest_data import DataOrchestrator
# from backend.utils.logger import get_logger

# from langchain_core.documents import Document
# from langchain.retrievers.document_compressors import LLMChainExtractor
# from langchain.retrievers import ContextualCompressionRetriever

# from dotenv import load_dotenv

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.constants import END
# from langgraph.graph import START, StateGraph, add_messages

# from typing import TypedDict, List, Annotated

# from langfuse.langchain import CallbackHandler

# import cohere
# import os

# load_dotenv()
# cohere_api = os.environ["COHERE_API"]

# langfuse_handler = CallbackHandler()

# llm = initialize_model()
# data = DataOrchestrator()
# retriever = data.get_db()
# logger = get_logger("main")
# compressor = LLMChainExtractor.from_llm(llm)
# compression_retriever = ContextualCompressionRetriever(base_compressor=compressor,
#                                                        base_retriever=retriever)  # extract only most relevant parts of retrieved documents

# co = cohere.ClientV2(api_key=cohere_api)

# class State(TypedDict):
#     question: str 
#     context: List[Document]
#     answer: str 
#     documents_reranked: list
#     messages: Annotated[list, add_messages]

# def retrieve(state: State):
#     try:
#         retrieved_docs = compression_retriever.invoke(input=state['messages'][-1].content)
#         logger.info("Successfully retrieved documents for the given question")
#         docs = [doc.page_content for doc in retrieved_docs]
#         response = co.rerank(
#             model="rerank-v3.5",
#             query=state['messages'][-1].content,
#             documents=docs,
#             top_n=3
#         )
#         reranked_docs = []
#         for result in response.results:
#             original_doc = retrieved_docs[result.index]
#             reranked_docs.append(original_doc)
        
#         logger.info(f"Successfully reranked documents. Top 3 scores: {[res.relevance_score for res in response.results]}")
#         return {"context": reranked_docs}
#     except Exception as e:
#         logger.error(f"Error during retrieval: {e}")
#         return {"context": []}

# def generate(state: State):
#     try:
#         docs_content = "\n\n".join(doc.page_content for doc in state["context"])
#         logger.info("Successfully extracted content from retrieved documents")
#         messages = create_chat_prompt(context=docs_content, question=state["messages"][-1])
#         response = llm.invoke(messages, config={'callbacks': [langfuse_handler]})
#         return {"answer": response.content}
#     except Exception as e:
#         logger.error(f"Failed to extract text from retrieved documents: {str(e)}")
#         return {"answer": ""}

# def create_graph():

#     graph_builder =  StateGraph(State).add_sequence(
#         [retrieve, generate]
#     )
#     graph_builder.add_edge(START, "retrieve")
#     graph_builder.add_edge("generate", END)
#     memory = MemorySaver()
#     graph = graph_builder.compile(checkpointer=memory)
#     return graph

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import START, StateGraph
from rag.nodes import retrieve, generate
from rag.state import State

def create_graph():
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph_builder.add_edge("generate", END)
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph