from rag.graph import create_graph

def run_pipeline(question: str) -> str:
    config = {"configurable": {"thread_id": "abc123"}}
    graph = create_graph()
    response = graph.invoke({"messages": question}, config=config)
    return response["answer"]