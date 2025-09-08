from langchain_core.prompts import ChatPromptTemplate


system_prompt = (
    """You are an AI assistant that answers user questions using the provided context.
The context consists of LangChain documentation. Always base your answers only on the given documents.
If the answer is not present in the documents, say you don’t know.
Context:
{context}

# Answer the user’s question as accurately and concisely as possible using only the context above.
# """
 )

def create_chat_prompt(context: str, question: str) -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}")
        ]
    )
    return prompt.invoke({"question": question, "context": context} )