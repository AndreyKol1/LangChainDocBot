from utils.logger import get_logger
from rag.prompt import create_chat_prompt, create_query_transformation_prompt
from rag.config import compression_retriever, co, llm, langfuse_handler  
from rag.state import State  

logger = get_logger("main")

def retrieve(state: State):
    try:
        prompt_refined = create_query_transformation_prompt(question=state['messages'][-1].content)
        improved_prompt = llm.invoke(prompt_refined, config={'callbacks': [langfuse_handler]})
        retrieved_docs = compression_retriever.invoke(input=improved_prompt.content)
        logger.info("Successfully retrieved documents for the given question")
        docs = [doc.page_content for doc in retrieved_docs]
        response = co.rerank(
            model="rerank-v3.5",
            query=improved_prompt.content,
            documents=docs,
            top_n=3
        )
        reranked_docs = []
        for result in response.results:
            original_doc = retrieved_docs[result.index]
            reranked_docs.append(original_doc)
        
        logger.info(f"Successfully reranked documents. Top 3 scores: {[res.relevance_score for res in response.results]}")
        return {"context": reranked_docs}
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        return {"context": []}

def generate(state: State):
    try:
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        logger.info("Successfully extracted content from retrieved documents")
        messages = create_chat_prompt(context=docs_content, question=state["messages"][-1])
        response = llm.invoke(messages, config={'callbacks': [langfuse_handler]})
        return {"answer": response.content}
    except Exception as e:
        logger.error(f"Failed to extract text from retrieved documents: {str(e)}")
        return {"answer": ""}
    