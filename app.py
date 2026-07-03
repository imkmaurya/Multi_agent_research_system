"""
Streamlit UI for the multi-agent research pipeline defined in pipeline.py

Run with:
    streamlit run app.py
"""

import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="ArgusCore | Multi-Agent Research System",
    page_icon="🟠",
    layout="wide",
)

# ---------- theme ----------
st.markdown(
    """
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    .stApp {
        background: radial-gradient(circle at 50% 0%, #17140f 0%, #0a0a0d 55%, #060607 100%);
    }
    .block-container { max-width: 1100px; padding-top: 3rem; }

    .eyebrow {
        text-align: center;
        color: #f97316;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.8rem;
        color: #f5f5f4;
    }
    .hero-title span { color: #f97316; }
    .hero-subtitle {
        text-align: center;
        color: #9c9c9f;
        font-size: 1rem;
        max-width: 620px;
        margin: 0 auto 2.4rem auto;
        line-height: 1.5;
    }

    .section-label {
        color: #f97316;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .panel-heading {
        color: #f5f5f4;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .stTextInput input {
        background: #131316 !important;
        color: #f5f5f4 !important;
        border: 1px solid #2a2a2e !important;
        border-radius: 8px !important;
    }
    .stTextInput input::placeholder { color: #6b6b70 !important; }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #101012;
        border: 1px solid #232326;
        border-radius: 14px;
    }

    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid #2a2a2e !important;
    }
    .run-btn button {
        background: linear-gradient(90deg, #f97316, #fb923c) !important;
        color: #0a0a0a !important;
        border: none !important;
        width: 100%;
    }
    .run-btn button:hover { filter: brightness(1.08); }
    .chip-btn button {
        background: #131316 !important;
        color: #b8b8bc !important;
        font-size: 0.78rem !important;
        padding: 0.25rem 0.7rem !important;
    }
    .chip-btn button:hover { border-color: #f97316 !important; color: #f97316 !important; }

    .agent-card {
        background: #101012;
        border: 1px solid #232326;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
    }
    .agent-card .top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .agent-name { color: #f5f5f4; font-weight: 700; font-size: 0.92rem; }
    .agent-desc { color: #8a8a8e; font-size: 0.8rem; margin-top: 0.15rem; }
    .badge {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        text-transform: uppercase;
    }
    .badge-waiting { background: #1c1c1f; color: #6b6b70; border: 1px solid #2a2a2e; }
    .badge-running { background: #3a2410; color: #fb923c; border: 1px solid #7c4a12; }
    .badge-done { background: #123a1f; color: #4ade80; border: 1px solid #1f6b38; }
    .badge-error { background: #3a1414; color: #f87171; border: 1px solid #6b1f1f; }

    .footer-note {
        text-align: center;
        color: #5c5c60;
        font-size: 0.78rem;
        margin-top: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

AGENTS = [
    ("01", "Search Agent", "Gathers recent web information"),
    ("02", "Reader Agent", "Scrapes & extracts deep content"),
    ("03", "Writer Chain", "Drafts the full research report"),
    ("04", "Critic Chain", "Reviews & scores the report"),
]

SUGGESTIONS = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress"]


def _set_topic(value: str) -> None:
    st.session_state.topic_input = value

# ---------- session state ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "status" not in st.session_state:
    st.session_state.status = "idle"  # idle | running | done | error
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""

# ---------- hero ----------
st.markdown('<div class="eyebrow">Multi-Agent AI System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Argus<span>Core</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Four specialized AI agents collaborate — searching, '
    'scraping, writing, and critiquing — to deliver a polished research report on any topic.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1], gap="large")

# ---------- left: input ----------
with left:
    st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)
    st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        label_visibility="collapsed",
    )

    st.markdown('<div class="run-btn">', unsafe_allow_html=True)
    run_clicked = st.button("⚡ Run Research Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:1.4rem;">Try</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTIONS))
    for col, suggestion in zip(chip_cols, SUGGESTIONS):
        with col:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            st.button(
                suggestion,
                key=f"chip_{suggestion}",
                use_container_width=True,
                on_click=_set_topic,
                args=(suggestion,),
            )
            st.markdown("</div>", unsafe_allow_html=True)

# ---------- right: pipeline status ----------
with right:
    st.markdown('<div class="panel-heading">Pipeline</div>', unsafe_allow_html=True)
    badge_class = {
        "idle": "badge-waiting",
        "running": "badge-running",
        "done": "badge-done",
        "error": "badge-error",
    }[st.session_state.status]
    badge_text = {
        "idle": "Waiting",
        "running": "Running",
        "done": "Done",
        "error": "Error",
    }[st.session_state.status]

    for num, name, desc in AGENTS:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="top-row">
                    <span class="agent-name">{num}&nbsp;&nbsp;{name}</span>
                    <span class="badge {badge_class}">{badge_text}</span>
                </div>
                <div class="agent-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- run pipeline ----------
if run_clicked:
    topic = st.session_state.topic_input.strip()
    if not topic:
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.status = "running"
        st.session_state.error_msg = ""
        with st.spinner("Agents are working on your topic..."):
            try:
                st.session_state.result = run_research_pipeline(topic)
                st.session_state.status = "done"
            except Exception as e:
                st.session_state.status = "error"
                st.session_state.error_msg = str(e)
        st.rerun()

if st.session_state.status == "error":
    st.error(f"Pipeline failed: {st.session_state.error_msg}")

# ---------- results ----------
result = st.session_state.result
if result and st.session_state.status == "done":
    st.divider()
    tab_report, tab_feedback, tab_search, tab_scrape = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(result.get("report", "_No report generated._"))
        st.download_button(
            "Download report as Markdown",
            data=result.get("report", ""),
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(result.get("feedback", "_No feedback generated._"))

    with tab_search:
        st.text(result.get("search_results", "_No search results captured._"))

    with tab_scrape:
        st.text(result.get("scrape_content", "_No scraped content captured._"))

st.markdown(
    '<div class="footer-note">ArgusCore · Powered by LangChain multi-agent pipeline · Built with Streamlit</div>',
    unsafe_allow_html=True,
)