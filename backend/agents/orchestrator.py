from backend.agents.retrieval_agent import retrieval_agent
from backend.agents.summary_agent import summary_agent
from backend.agents.citation_agent import citation_agent
from backend.agents.report_agent import report_agent


def run_agents(query):

    docs = retrieval_agent(query)

    answer = summary_agent(query, docs)

    citations = citation_agent(docs)

    final_report = report_agent(
        query=query,
        answer=answer,
        citations=citations
    )

    return final_report