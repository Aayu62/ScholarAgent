import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

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

.agent-box {
    padding: 0.8rem;
    border-radius: 8px;
    background-color: #1B2230;
    border-left: 4px solid #5B8DEF;
    margin-bottom: 0.8rem;
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

        with st.spinner("Processing PDF..."):
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
    st.subheader("Documents")
    st.write("Uploaded PDFs are indexed into the active FAISS knowledge base.")

    st.markdown("---")
    st.subheader("Session")
    st.write("Active")

col1, col2 = st.columns([3, 1])

with col1:
    st.title("ScholarAgent")
    st.caption("Multi-Agent AI Research Assistant")
    st.markdown("### Research Workspace")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            sources = message.get("sources", [])
            if sources:
                with st.expander("Retrieved sources"):
                    for index, source in enumerate(sources, start=1):
                        st.markdown(f"**Source {index}**")
                        st.write(source)

    prompt = st.chat_input("Ask questions about your uploaded documents...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "sources": []
        })

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching your documents..."):
                try:
                    response = requests.post(
                        f"{API_URL}/query",
                        params={"query": prompt},
                        timeout=120
                    )
                    response.raise_for_status()
                    result = response.json()
                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])
                except requests.RequestException as exc:
                    answer = f"Query failed: {exc}"
                    sources = []

            st.write(answer)
            if sources:
                with st.expander("Retrieved sources"):
                    for index, source in enumerate(sources, start=1):
                        st.markdown(f"**Source {index}**")
                        st.write(source)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

with col2:
    st.markdown("## Agents")

    st.markdown("""
    <div class="agent-box">
    Retrieval Agent<br>
    Searching semantic chunks
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    Summary Agent<br>
    Generating concise insights
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    Citation Agent<br>
    Extracting references
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    Report Agent<br>
    Creating structured output
    </div>
    """, unsafe_allow_html=True)
