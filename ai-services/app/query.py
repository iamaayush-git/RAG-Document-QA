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
# embeddings = OpenAIEmbeddings(
#     model="",
#     openai_api_base = os.getenv("OPENAI_API_BASE"),
#     openai_api_key = os.getenv("OPENAI_API_KEY")
# )

llm = ChatOpenAI(
    model="meituan/longcat-flash-chat:free",
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
    print(response)
    return {
        "success":True,
        "result":response
    }



    # # retrieved = vectorstores.similarity_search(question, k=k)
    # # Prepare concatenated context
    # contexts = [doc.page_content for doc, score in retrieved]
    # context_text = "\n\n---\n\n".join(contexts)
    # prompt = PromptTemplate(input_variables=["context", "question"], template=PROMPT)
    # # LLM choice: OpenAI by default, requires OPENAI_API_KEY. Could be replaced with local model.
    # llm = OpenAI(temperature=0)
    # chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=store.vs.as_retriever(search_type="similarity", search_kwargs={"k": k}), return_source_documents=True)
    # result = chain({"query": question})
    # # return both generated answer and retrieved docs
    # return {
    #     "answer": result.get("result"),
    #     "retrieved": [
    #         {"content": d.page_content, "metadata": d.metadata} for d in result.get("source_documents", [])
    #     ],
    # }
