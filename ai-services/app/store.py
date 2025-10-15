# ai-service/app/store.py
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from typing import List
from langchain.schema import Document

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")
EMBED_MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

class FaissStore:
    _instance = None

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        # If index exists, load, else create empty
        if os.path.exists(INDEX_PATH):
            self.vs = FAISS.load_local(INDEX_PATH, self.embeddings)
        else:
            self.vs = FAISS.from_documents([], self.embeddings)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FaissStore()
        return cls._instance

    def add_documents(self, documents: List[Document]) -> int:
        n = self.vs.add_documents(documents)
        self.vs.save_local(INDEX_PATH)
        return n

    def similarity_search(self, query: str, k=4):
        return self.vs.similarity_search_with_score(query, k=k)
