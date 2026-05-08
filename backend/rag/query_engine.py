from backend.rag.vector_store import load_vector_store

def retrieve_chunks(query):
    vector_store = load_vector_store()
    docs = vector_store.similarity_search(
        query,
        k=4
    )
    return docs