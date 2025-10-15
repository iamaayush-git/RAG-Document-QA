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

# import os
# from typing import Optional
# from pathlib import Path

# def load_text_from_file(filepath: str) -> str:
#     p = Path(filepath)
#     if not p.exists():
#         raise FileNotFoundError(f"{filepath} not found")
#     ext = p.suffix.lower()
#     if ext in [".txt", ".md"]:
#         return p.read_text(encoding="utf-8")
#     elif ext == ".pdf":
#         return extract_text_from_pdf(str(p))
#     else:
#         raise ValueError("Unsupported file type")

# def extract_text_from_pdf(path: str) -> str:
#     # Simple PDF extraction using PyPDF2 (robust libs: pdfplumber or PyMuPDF)
#     import PyPDF2
#     text_chunks = []
#     with open(path, "rb") as f:
#         reader = PyPDF2.PdfReader(f)
#         for page in reader.pages:
#             text_chunks.append(page.extract_text() or "")
#     return "\n".join(text_chunks)
