# langchain_utils.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda
import os
from .chroma_utils import vectorstore
from dotenv import load_dotenv
load_dotenv()


# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})



def get_rag_chain(model="gemini-2.5-flash"):

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model=model,
        api_key=os.getenv("GOOGLE_API_KEY"))

    
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    # LLM pipeline for contextualization
    contextualize_chain = contextualize_q_prompt | llm | StrOutputParser()

    # -----------------------------------------------------
    # 2. HISTORY-AWARE RETRIEVER
    # -----------------------------------------------------
    def history_aware_retriever(inputs):
        # Create standalone question
        standalone_question = contextualize_chain.invoke({
            "input": inputs["input"],
            "chat_history": inputs["chat_history"]
        })

        # Retrieve documents
        docs = retriever.invoke(standalone_question)

        # Combine context
        return {
            "context": "\n\n".join([d.page_content for d in docs]),
            "input": inputs["input"],
            "chat_history": inputs["chat_history"]
        }

    history_aware_retriever_runnable = RunnableLambda(history_aware_retriever)

   
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the provided context to answer accurately."),
        ("system", "Context:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    qa_chain = qa_prompt | llm | StrOutputParser()

   
    rag_chain = RunnableSequence(
        first=history_aware_retriever_runnable,
        last=qa_chain
    )

    return rag_chain



def convert_chat_history(history_rows):
    """
    Convert stored DB rows into LangChain message objects.
    history_rows should be a list of dicts with:
        { "role": "user"/"assistant", "content": "..."}
    """

    converted = []
    for row in history_rows:
        if row["role"] == "user":
            converted.append(HumanMessage(content=row["content"]))
        else:
            converted.append(AIMessage(content=row["content"]))

    return converted
