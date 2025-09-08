from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


system_prompt = (
    """You are an AI assistant that answers user questions using the provided context.
The context consists of LangChain documentation. Always base your answers only on the given documents.
If the answer is not present in the documents, say you don’t know.
Context:
{context}

# Answer the user’s question as accurately and concisely as possible using only the context above.
# """
 )

query_transformation_prompt = (
    """You are an AI assistant that specializes on query transformation. Given the user question: {question}
    Generate one alternative version that express the same information need but with different wording.
    Don't use any other words except refrased question:
"""
)

def create_chat_prompt(context: str, question: str) -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}")
        ]
    )
    return prompt.invoke({"question": question, "context": context} )

def create_query_transformation_prompt(question: str):
    expansion_prompt = PromptTemplate(
        input_variables=["question"],
        template=query_transformation_prompt
    )
    return expansion_prompt.invoke({"question": question})