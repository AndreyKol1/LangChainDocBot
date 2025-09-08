from scripts.retrieve_data import FetchFilesFromGitHub
import os

if len(os.listdir('data/raw')) == 0:
    fetcher = FetchFilesFromGitHub()
    fetcher.get_documents_from_github() # if directory is empty, fetch files from github repop

from rag.graph import create_graph

def run_pipeline(question: str) -> str:
    config = {"configurable": {"thread_id": "abc123"}}
    graph = create_graph()
    response = graph.invoke({"messages": question}, config=config)
    return response["answer"]