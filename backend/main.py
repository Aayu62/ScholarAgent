import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.rag.pdf_processor import process_pdf
from backend.rag.vector_store import create_vector_store
from backend.rag.query_engine import retrieve_chunks

app = FastAPI(title="ScholarAgent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message" : "ScholarAgent Backend Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = process_pdf(file_path)
    create_vector_store(chunks)
    return {
        "message" : "PDF processed succesfully",
        "chunks" : len(chunks)
    }

@app.post("/query")
async def query_rag(query: str):
    docs = retrieve_chunks(query)
    results = []

    for doc in docs:
        results.append(doc.page_content)

    return {
        "query" : query,
        "results" : results
    }