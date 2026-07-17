import os
import time
from pathlib import Path
from dotenv import load_dotenv

import streamlit as st

from langchain_community.vectorstores import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from ingest import build_vector_store

load_dotenv()

DB_PATH = ".chroma_db"
DATA_FOLDER = "data"
LLM_MODEL = "gemini-2.0-flash"
EMBED_MODEL = "models/gemini-embedding-001"

Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

# ============================================================
# BACKEND
# ============================================================

@st.cache_resource
def initialize_rag_backend():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, None

    os.environ["GOOGLE_API_KEY"] = api_key

    if not os.path.exists(DB_PATH):
        return None, None

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)

    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 6})

    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.3)

    return retriever, vector_store, llm


def get_workspace_stats(vector_store):
    """Return (doc_count, chunk_count) safely, defaulting to 0 if unavailable."""
    num_docs = 0
    num_chunks = 0
    try:
        num_docs = len(list(Path(DATA_FOLDER).glob("*.pdf")))
    except Exception:
        pass
    try:
        if vector_store is not None:
            num_chunks = vector_store._collection.count()
    except Exception:
        pass
    return num_docs, num_chunks


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IntelliDocs AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]{ font-family:'Inter',sans-serif; }
[data-testid="stAppViewContainer"]{ background:#090B11; }
[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:1.5rem; padding-bottom:2rem; max-width:1400px; }
#MainMenu{ visibility:hidden; }
footer{ visibility:hidden; }
header{ visibility:hidden; }
[data-testid="stSidebar"]{ background:#0E1422; border-right:1px solid rgba(255,255,255,.06); }
[data-testid="stSidebar"] *{ color:white; }
.card{ background:#111827; border:1px solid rgba(255,255,255,.06); border-radius:22px; padding:28px; transition:.35s; box-shadow:0 15px 40px rgba(0,0,0,.25); }
.card:hover{ transform:translateY(-6px); box-shadow:0 25px 60px rgba(0,0,0,.35); }
.hero{ background:linear-gradient(135deg,#172554,#111827,#1e293b); border-radius:28px; padding:45px; border:1px solid rgba(255,255,255,.08); margin-bottom:28px; }
.hero-title{ font-size:42px; font-weight:800; color:white; margin-bottom:10px; }
.hero-sub{ font-size:22px; font-weight:500; color:#CBD5E1; margin-bottom:20px; }
.hero-desc{ font-size:17px; color:#94A3B8; line-height:1.8; }
.metric-card{ background:#111827; padding:24px; border-radius:20px; border:1px solid rgba(255,255,255,.06); transition:.3s; min-height:190px; display:flex; flex-direction:column; justify-content:center; }
.metric-card:hover{ transform:translateY(-5px); border-color:#3B82F6; }
.metric-icon{ font-size:34px; margin-bottom:15px; }
.metric-value{ font-size:34px; font-weight:800; color:white; }
.metric-title{ font-size:16px; color:#94A3B8; margin-top:8px; }
.metric-desc{ font-size:14px; color:#64748B; }
.upload-card{ background:#111827; border-radius:22px; padding:30px; border:1px solid rgba(255,255,255,.06); }
.chat-card{ background:#111827; border-radius:22px; padding:25px; border:1px solid rgba(255,255,255,.06); }
.stButton>button{ width:100%; height:52px; border:none; border-radius:12px; font-weight:700; background:linear-gradient(90deg,#3B82F6,#6366F1); color:white; transition:.3s; }
.stButton>button:hover{ transform:translateY(-3px); }
[data-testid="stChatInput"]{ border-radius:18px; }
hr{ border-color:rgba(255,255,255,.05); }
.navbar{ display:flex; justify-content:space-between; align-items:center; padding:20px 28px; background:rgba(17,24,39,.75); backdrop-filter:blur(18px); border:1px solid rgba(255,255,255,.08); border-radius:22px; margin-bottom:25px; }
.logo{ font-size:34px; font-weight:800; color:white; }
.logo span{ color:#60A5FA; }
.nav-right{ display:flex; gap:15px; }
.badge{ padding:10px 18px; border-radius:30px; background:#172554; color:white; font-size:14px; font-weight:600; }
.analytics{ background:#111827; border-radius:24px; padding:25px; border:1px solid rgba(255,255,255,.06); margin-top:30px; }
.analytics-title{ font-size:28px; font-weight:700; color:white; margin-bottom:20px; }
.stat{ background:#0F172A; padding:18px; border-radius:16px; text-align:center; transition:.35s; border:1px solid rgba(255,255,255,.05); min-height:96px; display:flex; flex-direction:column; justify-content:center; }
.stat:hover{ transform:translateY(-6px); border-color:#3B82F6; }
.stat-number{ font-size:34px; font-weight:800; color:white; }
.stat-label{ font-size:14px; color:#94A3B8; margin-top:8px; }
.footer{ margin-top:60px; padding:30px; text-align:center; color:#64748B; font-size:14px; }
.source-chunk{ background:#0F172A; padding:18px; border-radius:15px; margin-bottom:18px; border:1px solid rgba(255,255,255,.06); }
.stats-spacer{ height:24px; }
.quick-action{
    display:block; text-decoration:none; background:#111827; color:#CBD5E1 !important;
    border:1px solid rgba(255,255,255,.08); border-radius:14px; padding:16px 18px;
    font-size:15px; font-weight:600; text-align:center; cursor:pointer; transition:.25s;
}
.quick-action:hover{ transform:translateY(-4px); border-color:#3B82F6; background:#172554; color:white !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# INIT BACKEND + SESSION STATE (single source of truth)
# ============================================================

retriever, vector_store, llm = (None, None, None)
backend_result = initialize_rag_backend()
if backend_result:
    retriever, vector_store, llm = backend_result

WELCOME_MSG = (
    "👋 Welcome to IntelliDocs AI.\n\n"
    "Upload documents, build the knowledge base, and ask natural "
    "language questions. I'll retrieve the most relevant chunks "
    "before generating every answer."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MSG}
    ]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("# 🧠 IntelliDocs AI")
    st.caption("Enterprise Knowledge Platform")
    st.markdown("---")

    if retriever and llm:
        st.success("🟢 System Online")
    else:
        st.error("🔴 Backend Not Ready")

    st.markdown("### AI Engine")
    st.info("Gemini 2.0 Flash")

    st.markdown("### Vector Database")
    st.info("ChromaDB")

    st.markdown("### Framework")
    st.info("LangChain")

    st.markdown("### Embeddings")
    st.info("Gemini Embedding")

    st.markdown("---")

    if st.button("🗑 Clear Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MSG}
        ]
        st.rerun()

    st.markdown("---")
    st.caption("Version 2.1")
    st.caption("© 2026 IntelliDocs AI")

# ============================================================
# NAVBAR + HERO
# ============================================================

st.markdown("""
<div class="navbar">
    <div class="logo">🧠 Intelli<span>Docs</span></div>
    <div class="nav-right">
        <div class="badge">Enterprise AI</div>
        <div class="badge">Knowledge Platform</div>
        <div class="badge">Gemini Powered</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 IntelliDocs AI</div>
    <div class="hero-sub">Enterprise Knowledge Intelligence Platform</div>
    <div class="hero-desc">
        Search, retrieve and analyze knowledge from your documents using
        Retrieval-Augmented Generation powered by Gemini AI.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# WORKSPACE ANALYTICS (dynamic)
# ============================================================

num_docs, num_chunks = get_workspace_stats(vector_store)

st.markdown("""
<div class="analytics">
    <div class="analytics-title">📈 Workspace Analytics</div>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-number">{num_docs}</div>
        <div class="stat-label">Documents Indexed</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-number">{num_chunks}</div>
        <div class="stat-label">Knowledge Chunks</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    health = "100%" if (retriever and llm) else "0%"
    st.markdown(f"""
    <div class="stat">
        <div class="stat-number">{health}</div>
        <div class="stat-label">System Health</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="stat">
        <div class="stat-number">24/7</div>
        <div class="stat-label">AI Availability</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="stats-spacer"></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📄</div>
        <div class="metric-value">{num_docs}</div>
        <div class="metric-title">Indexed Documents</div>
        <div class="metric-desc">Knowledge Base Ready</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-value">Gemini</div>
        <div class="metric-title">LLM Engine</div>
        <div class="metric-desc">Gemini 2.0 Flash</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">Chroma</div>
        <div class="metric-title">Vector Database</div>
        <div class="metric-desc">Persistent Storage</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    status = "ONLINE" if (retriever and llm) else "OFFLINE"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{"🟢" if status == "ONLINE" else "🔴"}</div>
        <div class="metric-value">{status}</div>
        <div class="metric-title">System Status</div>
        <div class="metric-desc">{"Ready" if status == "ONLINE" else "Check API key / DB"}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="stats-spacer"></div>', unsafe_allow_html=True)

# ============================================================
# KNOWLEDGE WORKSPACE
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<h2 style='color:white;font-size:32px;font-weight:700;margin-bottom:25px'>
Knowledge Workspace
</h2>
""", unsafe_allow_html=True)

left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("""
    <div class="card">
        <h3 style="color:white;margin-bottom:8px;">📂 Active Knowledge Base</h3>
        <p style="color:#94A3B8;font-size:16px;">
        Your indexed documents are stored inside ChromaDB and
        retrieved dynamically using semantic similarity search.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if os.path.exists(DB_PATH):
        st.success("✅ Knowledge Base Ready")
    else:
        st.error("Knowledge Base Not Found — upload a PDF and build it below")

with right:
    st.markdown("""
    <div class="card">
        <h3 style="color:white;">⚙ AI Stack</h3>
        <br>🧠 Gemini 2.0 Flash<br><br>
        ⚡ LangChain<br><br>
        📦 ChromaDB<br><br>
        🔎 Semantic Retrieval
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# UPLOAD DOCUMENTS
# ============================================================

st.markdown("<br><div id='upload-anchor'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color:white;font-size:30px;font-weight:700;'>Upload Documents</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="upload-card">
    <h3 style="color:white;margin-bottom:10px;">📄 Knowledge Base Builder</h3>
    <p style="color:#94A3B8;">
    Upload PDF files to expand your AI assistant's knowledge.
    The vector database will automatically rebuild after processing.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_pdf = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

if uploaded_pdf is not None:
    st.markdown(f"""
    <div class="card">
        <h3 style="color:white;">📄 {uploaded_pdf.name}</h3>
        <p style="color:#94A3B8;">
        Your document has been uploaded successfully and is ready for semantic indexing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    save_path = Path(DATA_FOLDER) / uploaded_pdf.name
    with open(save_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("File Size", f"{round(uploaded_pdf.size / 1024, 1)} KB")
    with colB:
        st.metric("Extension", "PDF")
    with colC:
        st.metric("Status", "Ready")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Build Knowledge Base"):
        with st.spinner("📚 Reading document and generating embeddings..."):
            try:
                build_vector_store()
                st.cache_resource.clear()
                st.session_state.kb_build_status = "success"
                st.rerun()
            except Exception as e:
                st.session_state.kb_build_status = f"error: {e}"
                st.rerun()

if st.session_state.get("kb_build_status") == "success":
    st.success("✅ Knowledge Base Updated Successfully — your document is now searchable!")
    del st.session_state["kb_build_status"]
elif isinstance(st.session_state.get("kb_build_status"), str) and st.session_state["kb_build_status"].startswith("error:"):
    st.error(st.session_state["kb_build_status"].replace("error: ", "", 1))
    del st.session_state["kb_build_status"]

# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h2 style='color:white;font-size:30px;font-weight:700;'>Quick Actions</h2>", unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)
with q1:
    st.markdown('<a href="#upload-anchor" class="quick-action">📂 Upload PDF</a>', unsafe_allow_html=True)
with q2:
    st.markdown('<a href="#upload-anchor" class="quick-action">⚡ Build Index</a>', unsafe_allow_html=True)
with q3:
    st.markdown('<a href="#ask-anchor" class="quick-action">💬 Ask Questions</a>', unsafe_allow_html=True)
with q4:
    st.markdown('<a href="#ask-anchor" class="quick-action">📑 View Sources</a>', unsafe_allow_html=True)

# ============================================================
# CONVERSATION WORKSPACE (single chat flow)
# ============================================================

st.markdown("<br><div id='ask-anchor'></div>", unsafe_allow_html=True)
st.markdown("""
<h2 style='color:white;font-size:30px;font-weight:700;margin-bottom:18px;'>
💬 Conversation Workspace
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-card">
    <h3 style="color:white;margin-bottom:5px;">AI Assistant</h3>
    <p style="color:#94A3B8;">
    Ask anything about your uploaded documents.
    Responses are generated using semantic retrieval and Gemini AI.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- render chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- single chat input ---
user_query = st.chat_input("Ask a question about your documents...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        if retriever is None or llm is None:
            error_text = (
                "⚠️ Backend not initialized. Check that your GOOGLE_API_KEY / "
                "GEMINI_API_KEY is set and that the knowledge base has been built."
            )
            st.error(error_text)
            st.session_state.messages.append({"role": "assistant", "content": error_text})
        else:
            try:
                with st.spinner("🔍 Searching vector database and generating answer..."):
                    matched_docs = retriever.invoke(user_query)
                    context = "\n\n".join(doc.page_content for doc in matched_docs)

                    prompt = f"""You are IntelliDocs AI.

Answer ONLY using the supplied context.

If the answer is unavailable, reply with:
"I couldn't find that information inside the uploaded documents."

--------------------
Context:
{context}
--------------------

Question:
{user_query}

Answer:"""

                    response = llm.invoke(prompt)
                    answer = response.content

                # stream the answer word by word (UI only, single pass)
                output = st.empty()
                displayed = ""
                for word in answer.split():
                    displayed += word + " "
                    output.markdown(displayed)
                    time.sleep(0.02)

                st.markdown("<br>", unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Chunks Used", len(matched_docs))
                with m2:
                    st.metric("AI Model", "Gemini")
                with m3:
                    st.metric("Status", "Completed")

                with st.expander("📚 Retrieved Knowledge Sources", expanded=False):
                    for i, doc in enumerate(matched_docs, 1):
                        st.markdown(f"""
                        <div class="source-chunk">
                            <h4 style="color:white;">Chunk {i}</h4>
                            <p style="color:#CBD5E1;line-height:1.8;">
                            {doc.page_content[:700]}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_text = f"Something went wrong: {e}"
                st.error(error_text)
                st.session_state.messages.append({"role": "assistant", "content": error_text})

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style="text-align:center;color:#64748B;font-size:14px;padding-bottom:10px;">
Built with ❤️ using <b>Gemini AI</b> • <b>LangChain</b> • <b>ChromaDB</b> • <b>Streamlit</b>
</div>
""", unsafe_allow_html=True)






