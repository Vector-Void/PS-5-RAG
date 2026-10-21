import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BG = "#0B0D0E"
SIDEBAR = "#101313"
PANEL = "#141919"
PANEL_HOVER = "#1B2221"
BORDER = "#293532"
TEXT = "#E8F0ED"
MUTED = "#91A09A"
ACCENT = "#64FFDA"
ACCENT_HOVER = "#8AFFE5"
BUTTON_TEXT = "#07110F"
INPUT_BG = "#111615"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    f"""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap'
    );

    :root {{
        color-scheme: dark;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {BG} !important;
        color: {TEXT} !important;
        font-family: 'DM Sans', sans-serif;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMain"] {{
        background: {BG};
    }}

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {{
        background: {SIDEBAR} !important;
    }}

    [data-testid="stSidebar"] {{
        border-right: 1px solid {BORDER};
    }}

    .block-container {{
        max-width: 1050px;
        padding-top: 2.2rem;
        padding-bottom: 5rem;
    }}

    h1, h2, h3, h4 {{
        color: {TEXT} !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.5px;
    }}

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {TEXT};
    }}

    [data-testid="stCaptionContainer"] {{
        color: {MUTED};
    }}

    hr {{
        border-color: {BORDER} !important;
    }}

    /* SIDEBAR BRAND */

    .sidebar-brand {{
        font-family: 'Space Grotesk', sans-serif;
        color: {TEXT};
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.7px;
        margin-bottom: 0.25rem;
    }}

    .sidebar-brand span,
    .hero-title span {{
        color: {ACCENT};
    }}

    .sidebar-subtitle {{
        color: {MUTED};
        font-size: 0.82rem;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }}

    .section-label {{
        color: {MUTED};
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin: 1.2rem 0 0.8rem;
    }}

    /* HERO */

    .hero-card {{
        background: linear-gradient(135deg, {PANEL}, #101B18);
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 1.7rem;
    }}

    .page-label {{
        color: {ACCENT};
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 0.7rem;
    }}

    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 700;
        letter-spacing: -1.5px;
        line-height: 1.15;
        color: {TEXT};
        margin-bottom: 0.9rem;
    }}

    .hero-description {{
        color: {MUTED};
        font-size: 0.96rem;
        line-height: 1.8;
        max-width: 650px;
    }}

    /* DOCUMENT CARDS */

    .document-card {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 0.9rem;
        margin: 0.65rem 0;
    }}

    .document-name {{
        color: {TEXT};
        font-size: 0.85rem;
        font-weight: 600;
        overflow-wrap: anywhere;
        line-height: 1.5;
    }}

    .document-meta {{
        color: {MUTED};
        font-size: 0.75rem;
        margin-top: 0.35rem;
    }}

    /* BUTTONS */

    .stButton > button {{
        background: {ACCENT} !important;
        color: {BUTTON_TEXT} !important;
        border: 1px solid {ACCENT} !important;
        border-radius: 10px !important;
        min-height: 2.65rem;
        font-weight: 700 !important;
        transition: all 0.2s ease;
    }}

    .stButton > button p,
    .stButton > button span,
    .stButton > button div {{
        color: {BUTTON_TEXT} !important;
    }}

    .stButton > button:hover {{
        background: {ACCENT_HOVER} !important;
        border-color: {ACCENT_HOVER} !important;
        transform: translateY(-1px);
    }}

    .stButton > button:focus {{
        box-shadow: 0 0 0 2px {BG}, 0 0 0 4px {ACCENT} !important;
    }}

    /* FILE UPLOADER */

    [data-testid="stFileUploader"] {{
        background: {PANEL};
        border: 1px dashed {BORDER};
        border-radius: 12px;
        padding: 0.65rem;
    }}

    [data-testid="stFileUploader"] section {{
        background: transparent;
    }}

    [data-testid="stFileUploader"] button {{
        background: {PANEL_HOVER} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}

    [data-testid="stFileUploader"] button p,
    [data-testid="stFileUploader"] button span {{
        color: {TEXT} !important;
    }}

    [data-testid="stFileUploader"] small {{
        color: {MUTED} !important;
    }}

    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {{
        background: transparent;
        border: none;
        padding: 1rem 0;
    }}

    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
        line-height: 1.8;
    }}

    [data-testid="stChatMessage"] p {{
        color: {TEXT};
    }}

    /* CHAT INPUT */

    [data-testid="stChatInput"] {{
        background: {INPUT_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 15px !important;
        box-shadow: none !important;
        transition: border-color 0.2s ease;
    }}

    [data-testid="stChatInput"]:focus-within {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 1px {ACCENT}30 !important;
    }}

    [data-testid="stChatInput"] textarea {{
        background: transparent !important;
        color: {TEXT} !important;
        caret-color: {ACCENT} !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: {MUTED} !important;
        opacity: 1 !important;
    }}

    [data-testid="stChatInput"] button {{
        background: {ACCENT} !important;
        color: {BUTTON_TEXT} !important;
        border-radius: 9px !important;
    }}

    [data-testid="stChatInput"] button svg {{
        fill: {BUTTON_TEXT} !important;
        color: {BUTTON_TEXT} !important;
    }}

    [data-testid="stChatInput"] button:hover {{
        background: {ACCENT_HOVER} !important;
    }}

    /* SOURCE REFERENCES */

    [data-testid="stExpander"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}

    [data-testid="stExpander"] summary {{
        color: {TEXT} !important;
    }}

    /* EMPTY STATE */

    .empty-state {{
        text-align: center;
        background: {PANEL};
        border: 1px dashed {BORDER};
        border-radius: 16px;
        padding: 2.3rem 1rem;
        margin: 1.5rem 0;
    }}

    .empty-icon {{
        font-size: 2rem;
        color: {ACCENT};
        margin-bottom: 0.7rem;
    }}

    .empty-title {{
        font-family: 'Space Grotesk', sans-serif;
        color: {TEXT};
        font-size: 1.1rem;
        font-weight: 600;
    }}

    .empty-description {{
        color: {MUTED};
        font-size: 0.86rem;
        line-height: 1.8;
        margin-top: 0.5rem;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    @media (max-width: 768px) {{
        .hero-card {{
            padding: 1.35rem;
        }}

        .hero-title {{
            font-size: 1.9rem;
        }}

        .block-container {{
            padding-top: 1.2rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# API FUNCTIONS
# --------------------------------------------------

def upload_pdf(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }

    try:
        response = requests.post(
            f"{API_URL}/documents/upload",
            files=files,
            timeout=180,
        )

        if response.ok:
            return response.json()

        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        raise RuntimeError(
            f"Upload failed ({response.status_code}): {detail}"
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            "Cannot connect to the backend. "
            "Make sure FastAPI is running."
        ) from exc


def ask_question(question):
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={
                "question": question,
                "top_k": 5,
            },
            timeout=180,
        )

        if response.ok:
            return response.json()

        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        raise RuntimeError(
            f"Query failed ({response.status_code}): {detail}"
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            "Cannot connect to the backend. "
            "Make sure FastAPI is running."
        ) from exc


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">RAG ASSISTANT<span>.</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-subtitle">
            Your documents, searchable through AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">DOCUMENT LIBRARY</div>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDFs containing extractable text.",
    )

    if st.button("＋ Upload Documents", use_container_width=True):

        if not uploaded_files:
            st.warning("Please select at least one PDF.")

        else:
            for uploaded_file in uploaded_files:

                already_uploaded = any(
                    document["filename"] == uploaded_file.name
                    for document in st.session_state.uploaded_documents
                )

                if already_uploaded:
                    st.info(
                        f"{uploaded_file.name} was already uploaded "
                        "during this session."
                    )
                    continue

                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        result = upload_pdf(uploaded_file)

                        document = {
                            "filename": result["filename"],
                            "pages": result["pages_extracted"],
                            "chunks": result["chunks_indexed"],
                        }

                        st.session_state.uploaded_documents.append(document)

                        st.success(
                            f"Successfully processed {document['filename']}"
                        )

                    except (RuntimeError, KeyError) as exc:
                        st.error(str(exc))

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">UPLOADED DOCUMENTS</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.uploaded_documents:
        for document in st.session_state.uploaded_documents:
            st.markdown(
                f"""
                <div class="document-card">
                    <div class="document-name">
                        📄 &nbsp; {document['filename']}
                    </div>
                    <div class="document-meta">
                        {document['pages']} pages
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"""
            <div style="
                color: {MUTED};
                font-size: 0.83rem;
                line-height: 1.7;
                padding: 0.5rem 0;
            ">
                No documents uploaded yet.<br>
                Your processed PDFs will appear here.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# MAIN HEADER
# Use st.html() to render HTML directly.
# --------------------------------------------------

st.html("""
<div class="hero-card">
    <div class="page-label">DOCUMENT INTELLIGENCE</div>
    <div class="hero-title">
        Ask your documents.<br>
        <span>Get grounded answers.</span>
    </div>
    <div class="hero-description">
        Upload your PDFs and ask questions in natural language.
        The system retrieves relevant passages and generates
        answers grounded in your document collection.
    </div>
</div>
""")


# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

st.markdown("### 💬 Conversation")

st.caption(
    "Ask questions about your uploaded documents. "
    "Source references appear with answers when available."
)

if not st.session_state.messages:
    st.html("""
    <div class="empty-state">
        <div class="empty-icon">⌕</div>
        <div class="empty-title">Start exploring your documents</div>
        <div class="empty-description">
            Upload a PDF using the sidebar, then type your question
            in the chat box below.<br>
            Answers are generated using retrieved document content.
        </div>
    </div>
    """)


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 View source references"):
                for source in message["sources"]:
                    filename = source.get("filename", "Unknown document")
                    page = source.get("page", "?")
                    st.markdown(f"**{filename}** · Page {page}")


# --------------------------------------------------
# CHAT INPUT AND RESPONSE
# --------------------------------------------------

question = st.chat_input("Ask a question about your documents...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents and generating an answer..."):
            try:
                result = ask_question(question)

                answer = result.get(
                    "answer",
                    "The backend returned no answer.",
                )

                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("📚 View source references"):
                        for source in sources:
                            filename = source.get(
                                "filename",
                                "Unknown document",
                            )
                            page = source.get("page", "?")
                            st.markdown(f"**{filename}** · Page {page}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except RuntimeError as exc:
                error_message = f"⚠️ {exc}"
                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                })