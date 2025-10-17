# ai-service/app/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
import shutil

from ingest import ingest_file
from query import ask_question, embeddings
from langchain_community.vectorstores import FAISS


app = FastAPI(title = "RAG AI service")

# cors congure
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IngestRequest(BaseModel):
  filepath:str

class AskQuestion(BaseModel):
  question:str
  k:int=2

@app.get("/")
def check():
  return {"success":True}

@app.post('/ingest')
async def ingest(file: UploadFile = File(...)):
  try:
    save_path = f"../uploaded/{file.filename}"
    os.makedirs("../uploaded", exist_ok = True)
    with open(save_path,"wb") as f:
      f.write(await file.read())

    result = ingest_file(save_path)
    os.remove(save_path)
    return {"success":True, "ingested":result}
  except Exception as e:
    raise HTTPException(status_code=500, detail="Something went wrong. Please try again later.")


@app.post("/ask")
async def ask(req: AskQuestion):
    try:
        # Check if FAISS index exists
        if not os.path.exists("faiss_index"):
            raise HTTPException(
                status_code=400, 
                detail="No documents ingested yet. Please upload files first."
            )

        # Call your question-answer function
        response = ask_question(question=req.question, k=req.k)
        print(response)
        return {"success": True, "answer": response.get("result")}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again later."
        )


@app.post("/reset")
async def reset_context():
    try:
        folder = "faiss_index"
        if os.path.exists(folder):
            shutil.rmtree(folder)
        return {"success": True, "message": "Context cleared"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again later.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
