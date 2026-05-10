import os

from backend.agents.orchestrator import run_agents

VECTOR_STORE_DIR = "data/vector_store"


def query_rag(query):
    if not os.path.exists(os.path.join(VECTOR_STORE_DIR, "index.faiss")):
        return {
            "query": query,
            "answer": "Please upload and process a PDF before asking questions.",
            "sources": []
        }

    result = run_agents(query)

    return {
        "query": query,
        "answer": result["summary"],
        "sources": result["citations"]
    }
