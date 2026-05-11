from datetime import datetime


def report_agent(query, answer, citations):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_citations = []

    for citation in citations:
        formatted_citations.append(
            f"[Source {citation['source']}] {citation['content']}"
        )

    report = {
        "query": query,
        "generated_at": timestamp,
        "summary": answer,
        "citations": formatted_citations
    }

    return report