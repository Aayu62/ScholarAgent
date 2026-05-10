def citation_agent(docs):
    citations = []
    for index, doc in enumerate(docs, start=1):
        citations.append({
            "source": index,
            "content": doc.page_content[:300]
        })

    return citations