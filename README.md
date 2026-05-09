# ScholarAgent

ScholarAgent is a document-first AI research assistant. Upload a PDF, then ask questions and get answers grounded in the document content using a Retrieval-Augmented Generation (RAG) pipeline.

This repository contains:
- A FastAPI backend for PDF ingestion, vector indexing, retrieval, and answering
- A Streamlit frontend that provides a chat UI with session history

## What It Does

1. Upload a PDF
   - The backend saves the PDF to `data/uploads/`
   - Text is extracted and split into overlapping chunks

2. Build a local vector index (FAISS)
   - Each chunk is embedded using `sentence-transformers/all-MiniLM-L6-v2`
   - Embeddings are stored in a local FAISS index under `data/vector_store/`

3. Ask questions (RAG chat)
   - The backend retrieves the top-k most relevant chunks for your query
   - Those chunks are used as context for a Gemini model call
   - The response is returned along with the retrieved source snippets

## Features (Day 1 to Day 3)

- PDF upload and processing
- Text extraction and chunking
- Local vector search with FAISS
- RAG-based Q&A with retrieved sources
- Streamlit chat UI with session memory (`st.session_state`)

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Frontend: Streamlit
- RAG / Retrieval: LangChain, FAISS (local), sentence-transformers (MiniLM)
- LLM: Google Gemini via `google-genai`

## Project Structure

```text
ScholarAgent/
  backend/
    main.py                  # FastAPI app (upload/query endpoints)
    llm/
      gemini_service.py      # Gemini client + prompt orchestration
    rag/
      pdf_processor.py       # PDF loading + chunking
      vector_store.py        # FAISS create/load
      query_engine.py        # Retrieval + context + answer
  frontend/
    app.py                   # Streamlit UI
  data/
    uploads/                 # Uploaded PDFs (local)
    vector_store/            # FAISS index files (local)
  requirements.txt
  README.md
```

## Setup

### 1. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file at the repo root:

```env
GEMINI_API_KEY=your_key_here

# Optional: override model (default is gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash
```

## Run Locally

### 1. Start the backend (FastAPI)

```powershell
uvicorn backend.main:app --reload
```

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Start the frontend (Streamlit)

```powershell
streamlit run frontend/app.py
```

Open: `http://127.0.0.1:8501`

## API Reference

### POST `/upload`

Uploads a PDF, extracts text, chunks it, and builds a FAISS index.

Example (PowerShell):

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/upload" `
  -Form @{ file = Get-Item ".\path\to\file.pdf" }
```

Response:

```json
{
  "message": "PDF processed succesfully",
  "chunks": 42
}
```

### POST `/query`

Runs retrieval over the FAISS index and returns a Gemini-generated answer grounded in retrieved chunks.

Example:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/query?query=What%20is%20this%20document%20about%3F"
```

Response:

```json
{
  "query": "What is this document about?",
  "answer": "...",
  "sources": ["...", "...", "...", "..."]
}
```

If no PDF has been uploaded yet (no vector index exists), the API returns a friendly message and empty sources.

## How RAG Works Here

- Chunking: `RecursiveCharacterTextSplitter` splits PDF text into overlapping chunks.
- Embedding: Each chunk is embedded using a lightweight sentence-transformer model (MiniLM).
- Vector search: FAISS retrieves the most similar chunks to your query.
- Answering: Gemini is prompted to answer using only the retrieved context.

## Notes and Limitations

- The vector store is currently a single local index at `data/vector_store/`.
  Uploading a new PDF overwrites the previous index (MVP behavior).
- `FAISS.load_local(..., allow_dangerous_deserialization=True)` is used for convenience in local development.
  Do not use that setting in untrusted environments.
- Retrieval currently returns raw chunk text as "sources". Citation formatting is a roadmap item.

## Troubleshooting

- `GEMINI_API_KEY is not configured.`
  - Set `GEMINI_API_KEY` in `.env` and restart the backend.

- Backend works, but Streamlit cannot connect
  - Confirm backend is running at `http://127.0.0.1:8000/`.
  - Check Windows firewall prompts.

- Slow first run
  - The embedding model may download on first use.
  - Configure a Hugging Face token (`HF_TOKEN`) for higher rate limits if needed.

## Roadmap (Upcoming Days)

- Day 4: Multi-agent workflow (CrewAI): retrieval agent, summarizer agent, citation agent, report agent
- Day 5: Report generation + better citation formatting + UI polish
- Day 6: Docker + deployment (backend + frontend)
- Day 7: Final polish, docs, demo assets, and resume-ready packaging
