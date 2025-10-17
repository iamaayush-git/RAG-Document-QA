# ai-service/app/ingest.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import load_file
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

# configure sizes for chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)

embeddings = GoogleGenerativeAIEmbeddings(
  model="models/gemini-embedding-001",
  google_api_key=os.getenv("GEMINI_API_KEY")
)

def ingest_file(filepath: str):
    """Parse file, split, embed and add to FAISS. Returns number of documents added."""
    docs = load_file(filepath)
    if not docs:
        raise ValueError("No text extracted from file")
    chunks = splitter.split_documents(docs)
    if os.path.exists("faiss_index/index.faiss"):
        vectorstores = FAISS.load_local("faiss_index",embeddings, allow_dangerous_deserialization=True)
        vectorstores.add_documents(chunks)
    else:
        vectorstores = FAISS.from_documents(chunks, embeddings)

    vectorstores.save_local("faiss_index")
    return len(chunks)
