# ai-service/app/query.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

prompt_template = """You are a helpful assistant. Use the context below to answer the question. If the answer is not contained in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer concisely and show sources at the end.
"""
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo-0613",
    openai_api_base = os.getenv("OPENAI_API_BASE"),
    openai_api_key = os.getenv("OPENAI_API_KEY")
)
embeddings = GoogleGenerativeAIEmbeddings(
  model="models/gemini-embedding-001",
  google_api_key=os.getenv("GEMINI_API_KEY")
)


def ask_question(question: str, k: int = 2):    
    vectorstores = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    retriever = vectorstores.as_retriever(
    search_type="similarity",
    search_kwargs = {"k":k},
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = retriever,
        chain_type_kwargs = {"prompt":prompt}
    )

    response = qa_chain.invoke(question)
    return response
