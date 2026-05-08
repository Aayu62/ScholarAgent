import streamlit as st

st.set_page_config(
    page_title="ScholarAgent",
    page_icon="📘",
    layout="wide"
)

# CUSTOM CSS
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

.chat-box {
    padding: 1rem;
    border-radius: 12px;
    background-color: #161B22;
    border: 1px solid #2A2F3A;
    margin-bottom: 1rem;
}

.agent-box {
    padding: 0.8rem;
    border-radius: 10px;
    background-color: #1B2230;
    border-left: 4px solid #5B8DEF;
    margin-bottom: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.title("📘 ScholarAgent")

    st.markdown("---")

    st.subheader("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload Research Papers",
        type=["pdf"]
    )

    st.markdown("---")

    st.subheader("Documents")

    st.markdown("""
    - DeepLearning.pdf
    - RAG_Research.pdf
    - Transformers.pdf
    """)

    st.markdown("---")

    st.subheader("Session")

    st.write("🟢 Active")

# MAIN LAYOUT
col1, col2 = st.columns([3, 1])
# CHAT AREA
with col1:

    st.title("ScholarAgent")

    st.caption("Multi-Agent AI Research Assistant")

    st.markdown("### Research Workspace")

    st.markdown("""
    <div class="chat-box">
    <b>User:</b> Compare RAG architectures discussed in uploaded papers.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-box">
    <b>ScholarAgent:</b><br><br>
    
    Based on the uploaded papers, Dense Passage Retrieval (DPR) improves semantic retrieval accuracy compared to traditional BM25 approaches. Hybrid RAG pipelines combining sparse and dense retrieval demonstrate better contextual grounding and lower hallucination rates.
    </div>
    """, unsafe_allow_html=True)

    st.text_input(
        "Ask ScholarAgent",
        placeholder="Ask questions about your uploaded documents..."
    )

# AGENT PANEL
with col2:

    st.markdown("## Agents")

    st.markdown("""
    <div class="agent-box">
    🔍 Retrieval Agent<br>
    Searching semantic chunks
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    🧠 Summary Agent<br>
    Generating concise insights
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    📚 Citation Agent<br>
    Extracting references
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-box">
    📝 Report Agent<br>
    Creating structured output
    </div>
    """, unsafe_allow_html=True)