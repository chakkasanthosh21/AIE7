from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import os
from aimakerspace.text_utils import TextFileLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from typing import Dict
import asyncio
from PyPDF2 import PdfReader
from pydantic import BaseModel
from aimakerspace.openai_utils.chatmodel import ChatOpenAI

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for vector DBs (keyed by doc/session id)
doc_vector_dbs: Dict[str, VectorDatabase] = {}

def generate_doc_id() -> str:
    import uuid
    return str(uuid.uuid4())

class QueryRequest(BaseModel):
    doc_id: str
    query: str
    k: int = 3

@app.post("/index-pdf/")
async def index_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        # Extract text directly using PyPDF2
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDF.")
        # Chunk text
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split(text)
        # Build vector DB
        vector_db = VectorDatabase()
        await vector_db.abuild_from_list(chunks)
        # Store in-memory with a doc id
        doc_id = generate_doc_id()
        doc_vector_dbs[doc_id] = vector_db
        return {"doc_id": doc_id, "num_chunks": len(chunks)}
    finally:
        os.remove(tmp_path)

@app.post("/query-pdf/")
async def query_pdf(request: QueryRequest = Body(...)):
    doc_id = request.doc_id
    query = request.query
    k = request.k
    if doc_id not in doc_vector_dbs:
        raise HTTPException(status_code=404, detail="Document not found.")
    vector_db = doc_vector_dbs[doc_id]
    # Retrieve top-k relevant chunks
    results = vector_db.search_by_text(query, k=k, return_as_text=True)
    context = "\n".join(results)
    # Use OpenAI LLM to answer the question with the retrieved context
    chat = ChatOpenAI()
    prompt = f"You are a helpful assistant. Use the following context to answer the user's question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    answer = chat.run([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])
    return {"answer": answer, "context": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 