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