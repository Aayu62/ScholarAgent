from backend.llm.gemini_service import generate_response

def summary_agent(query,docs):
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    answer = generate_response(query, context)
    return answer