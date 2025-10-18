# ai-service/app/utils.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from pathlib import Path

def load_file(filepath):
    p = Path(filepath).resolve()
    if not p.exists():
        raise FileNotFoundError(f"{filepath} not found")
    if filepath.endswith(".pdf"):
        print("PDF")
        return PyPDFLoader(filepath).load()
    if filepath.endswith(".txt"):
        return TextLoader(filepath).load()
    if filepath.endswith(".md"):
        return UnstructuredMarkdownLoader(filepath).load()
    else:
        raise ValueError("Unsupported file type")

