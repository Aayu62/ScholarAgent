from backend.rag.vector_store import load_vector_store

def retrieval_agent(query, k=4):
    vector_store = load_vector_store()

    docs = vector_store.similarity_search(
        query,
        k=k
    )

    return docs