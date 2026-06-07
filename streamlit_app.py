"""
AIDEOM-VN · Streamlit Wrapper
=============================
Streamlit app for hosting the multi-page AIDEOM-VN website on Streamlit Cloud.

Architecture:
- Use streamlit.components.v1.html to embed each HTML page
- Sidebar lets user pick which bài to view
- Reads HTML files directly from the same directory

Deploy:
    streamlit run streamlit_app.py

Or on Streamlit Cloud:
    1. Push this folder to GitHub
    2. Connect repo at share.streamlit.io
    3. Set main file = streamlit_app.py
"""
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# =============================================================
# CONFIG
# =============================================================
st.set_page_config(
    page_title="AIDEOM-VN · AI Decision Optimization Model for Vietnam",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent

EXERCISES = [
    {"id": 0,  "title": "🏠 Trang chủ",                   "file": "index.html",  "section": "Trang chủ"},
    {"id": 1,  "title": "Bài 1 · Cobb-Douglas mở rộng",    "file": "bai01.html",  "section": "Phần A · Cơ bản"},
    {"id": 2,  "title": "Bài 2 · LP phân bổ ngân sách",    "file": "bai02.html",  "section": "Phần A · Cơ bản"},
    {"id": 3,  "title": "Bài 3 · LP priority 10 ngành",    "file": "bai03.html",  "section": "Phần A · Cơ bản"},
    {"id": 4,  "title": "Bài 4 · LP ngành-vùng 6×4",       "file": "bai04.html",  "section": "Phần B · Trung bình"},
    {"id": 5,  "title": "Bài 5 · MIP chọn 15 dự án",       "file": "bai05.html",  "section": "Phần B · Trung bình"},
    {"id": 6,  "title": "Bài 6 · TOPSIS 6 vùng",           "file": "bai06.html",  "section": "Phần B · Trung bình"},
    {"id": 7,  "title": "Bài 7 · NSGA-II Pareto",          "file": "bai07.html",  "section": "Phần B · Trung bình"},
    {"id": 8,  "title": "Bài 8 · Dynamic Programming",    "file": "bai08.html",  "section": "Phần B · Trung bình"},
    {"id": 9,  "title": "Bài 9 · AI Labor Impact",         "file": "bai09.html",  "section": "Phần C · Khó"},
    {"id": 10, "title": "Bài 10 · Stochastic 2-stage",    "file": "bai10.html",  "section": "Phần C · Khó"},
    {"id": 11, "title": "Bài 11 · Q-learning RL",          "file": "bai11.html",  "section": "Phần C · Khó"},
    {"id": 12, "title": "Bài 12 · AIDEOM Integration",     "file": "bai12.html",  "section": "Phần D · Integration"},
]


# =============================================================
# SIDEBAR NAVIGATION
# =============================================================
st.sidebar.markdown(
    """
    <div style="background:linear-gradient(135deg,#06b6d4,#a855f7,#ec4899);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                font-size:24px;font-weight:900;margin-bottom:8px">
    🚀 AIDEOM-VN
    </div>
    <div style="color:#94a3b8;font-size:11px;margin-bottom:18px;line-height:1.5">
    AI Decision Optimization Model for Vietnam<br>
    12 bài đề tài cuối kỳ
    </div>
    """,
    unsafe_allow_html=True,
)

# Group by section
sections = {}
for ex in EXERCISES:
    sections.setdefault(ex["section"], []).append(ex)

selected_id = st.session_state.get("selected_id", 0)

for sec_name, items in sections.items():
    if sec_name != "Trang chủ":
        st.sidebar.markdown(
            f"<div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:14px 0 4px;padding:0 8px'>{sec_name}</div>",
            unsafe_allow_html=True,
        )
    for ex in items:
        label = ex["title"]
        if st.sidebar.button(label, key=f"nav_{ex['id']}", use_container_width=True):
            st.session_state.selected_id = ex["id"]
            selected_id = ex["id"]
            st.rerun()


# =============================================================
# RENDER PAGE
# =============================================================
selected = next((e for e in EXERCISES if e["id"] == selected_id), EXERCISES[0])
html_file = ROOT / selected["file"]

if not html_file.exists():
    st.error(f"⚠ Không tìm thấy file: {selected['file']}")
    st.stop()

# Read HTML
html_content = html_file.read_text(encoding="utf-8")

# Inject base URL so that local CSS/JS still resolve (streamlit serves them differently)
# For Streamlit Cloud, we need to inline styles + scripts.
def inline_local_assets(html: str) -> str:
    """Replace <link rel='stylesheet' href='styles.css'> and <script src='...'>
    with inline content so the iframe can render everything self-contained."""
    css_file = ROOT / "styles.css"
    data_file = ROOT / "data.js"
    shared_file = ROOT / "shared.js"
    chatbot_file = ROOT / "chatbot.js"

    if css_file.exists():
        html = html.replace(
            '<link rel="stylesheet" href="styles.css">',
            f"<style>\n{css_file.read_text(encoding='utf-8')}\n</style>",
        )
    if data_file.exists():
        html = html.replace(
            '<script src="data.js"></script>',
            f"<script>\n{data_file.read_text(encoding='utf-8')}\n</script>",
        )
    if shared_file.exists():
        html = html.replace(
            '<script src="shared.js"></script>',
            f"<script>\n{shared_file.read_text(encoding='utf-8')}\n</script>",
        )
    if chatbot_file.exists():
        html = html.replace(
            '<script src="chatbot.js"></script>',
            f"<script>\n{chatbot_file.read_text(encoding='utf-8')}\n</script>",
        )
    return html


html_content = inline_local_assets(html_content)

# Hide Streamlit default chrome for cleaner look
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }
        section[data-testid="stSidebar"] button {
            background: rgba(15,23,42,0.4) !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(168,85,247,0.2) !important;
            font-size: 13px !important;
            text-align: left !important;
            padding: 8px 12px !important;
            margin-bottom: 2px !important;
        }
        section[data-testid="stSidebar"] button:hover {
            background: rgba(168,85,247,0.15) !important;
            border-color: #a855f7 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render full HTML in iframe (height matches typical page content)
components.html(html_content, height=2400, scrolling=True)
