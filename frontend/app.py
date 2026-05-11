import requests
import streamlit as st


API_URL = "http://backend:8000"

st.set_page_config(
    page_title="ScholarAgent",
    page_icon="SA",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

section[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #2A2F3A;
}

h1, h2, h3 {
    color: white;
}

.stTextInput input {
    background-color: #1E2430;
    color: white;
    border: 1px solid #313846;
}

.stTextArea textarea {
    background-color: #1E2430;
    color: white;
}
.agent-card {
    background-color: #161B22; 
    padding: 12px;
    border-radius: 6px;
    text-align: center;
    margin-bottom: 8px;
    color: #ffffff;
    font-size: 14px;
    line-height: 1.4;
    border: 1px solid #2A2F3A;
}



</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Upload a PDF, then ask me questions about it.",
            "sources": []
        }
    ]

with st.sidebar:
    st.title("ScholarAgent")
    st.markdown("---")
    st.subheader("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload Research Papers",
        type=["pdf"]
    )

    if uploaded_file is not None:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("Processing PDF and building vector index..."):
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=120
                )
            except requests.RequestException as exc:
                st.error(f"Upload failed: {exc}")
            else:
                if response.status_code == 200:
                    result = response.json()
                    st.success("PDF processed successfully. You can ask questions now.")
                    st.json(result)
                else:
                    st.error(f"Upload failed: {response.text}")

    st.markdown("---")
    st.subheader("Knowledge Base")
    st.write("Uploaded PDFs are indexed into the active FAISS knowledge base.")
    st.markdown("---")
    st.subheader("Session Status")
    st.write("Active")

st.title("ScholarAgent")
st.caption("Multi-Agent AI Research Assistant")
st.markdown("### Research Workspace")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        citations = message.get("citations", [])
        
        if citations:
            st.markdown("### Citations")   
            for citation in citations:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#1B2230;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        border-left:4px solid #5B8DEF;
                    ">
                    {citation}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
prompt = st.chat_input("Ask questions about your uploaded documents...")
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "citations": []
    })
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Retrieval Agent searching vector database..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    params={"query": prompt},
                    timeout=120
                )
                response.raise_for_status()
                result = response.json()
                st.info("Summary Agent generating response...")
                answer = result.get("answer", "No answer returned.")
                citations = result.get("citations", [])
            except requests.RequestException as exc:
                answer = f"Query failed: {exc}"
                citations = []
        st.markdown(answer)
        if citations:
            st.markdown("### Citations")
            for citation in citations:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#1B2230;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        border-left:4px solid #5B8DEF;
                    ">
                    {citation}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        report_text = f"""
        ScholarAgent Research Report
        
        Query:
        {prompt}
        
        Generated Answer:
        {answer}
        
        Citations:
        """
        
        for citation in citations:
            report_text += f"\n- {citation}\n"
        
        st.download_button(
            label="Download Research Report",
            data=report_text,
            file_name="scholaragent_report.txt",
            mime="text/plain"
        )
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": citations
    })

st.markdown("---")
st.markdown("## Active AI Agents")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="agent-card">
    🔍<br><br>
    <b>Retrieval Agent</b><br>
    Semantic Search
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
    🧠<br><br>
    <b>Summary Agent</b><br>
    AI Reasoning
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
    📚<br><br>
    <b>Citation Agent</b><br>
    Source Extraction
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="agent-card">
    📝<br><br>
    <b>Report Agent</b><br>
    Research Reports
    </div>
    """, unsafe_allow_html=True)