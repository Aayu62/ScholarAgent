import os

from backend.rag.vector_store import load_vector_store
from backend.llm.gemini_service import generate_response

VECTOR_STORE_DIR = "data/vector_store"


def query_rag(query):
    if not os.path.exists(os.path.join(VECTOR_STORE_DIR, "index.faiss")):
        return {
            "query": query,
            "answer": "Please upload and process a PDF before asking questions.",
            "sources": []
        }

    vector_store = load_vector_store()

    docs = vector_store.similarity_search(
        query,
        k=4
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    answer = generate_response(query, context)

    return {
        "query": query,
        "answer": answer,
        "sources": [doc.page_content for doc in docs]
    }
