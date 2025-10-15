# ai-service/app/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from ingest import ingest_file
from query import ask_question
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "RAG AI service")

# cors congure
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
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
    # os.remove(save_path)
    return {"success":True, "ingested":result}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
async def ask(req:AskQuestion):
  try:
    response = ask_question(question=req.question, k = req.k)
    return response
  except Exception as e:
    return HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from query import ask_question
# import uvicorn
# from ingest import ingest_file

# app = FastAPI(title="RAG AI Service")

# class IngestRequest(BaseModel):
#     filepath: str

# class AskRequest(BaseModel):
#     question: str
#     k: int = 4

# @app.post("/ingest")
# async def ingest(req: IngestRequest):
#     try:
#         result = ingest_file(req.filepath)
#         return {"ok": True, "ingested": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/ask")
# async def ask(req: AskRequest):
#     try:
#         resp = ask_question(req.question, k=req.k)
#         return resp
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
