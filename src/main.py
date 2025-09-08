from .rag.pipeline import run_pipeline

def ask_question(question: str) -> str:
    answer = run_pipeline(question)
    return answer
