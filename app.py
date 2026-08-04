"""
RAG Chatbot — University Services (Premium UI)
Streamlit app kết nối RAG Retrieval (Task 9) và Generation (Task 10).

Chạy:
    streamlit run app.py
"""

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Thêm project root vào sys.path để import các task từ src/
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.task10_generation import generate_with_citation

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="HR & Legal RAG Chatbot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# PREMIUM CSS — targeting Streamlit internal classes
# =============================================================================

st.markdown("""
<style>
/* ─── Google Font ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ─── Global App Background ─── */
.stApp {
    background: #0e0e11;
    font-family: 'Inter', sans-serif;
}

/* ─── Sidebar ─── */
section[data-testid="stSidebar"] {
    background: #0e0e11;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span {
    color: #c8c8e0 !important;
}

/* ─── Sidebar suggestion buttons ─── */
section[data-testid="stSidebar"] button[kind="secondary"] {
    background: rgba(99, 102, 241, 0.12) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    color: #a5b4fc !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    font-size: 0.82rem !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(99, 102, 241, 0.28) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
}

/* ─── Chat messages ─── */
.stChatMessage {
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    animation: fadeInUp 0.4s ease-out;
}

/* User message */
.stChatMessage[data-testid="stChatMessage"]:has(.stMarkdown) {
    transition: all 0.3s ease;
}

/* ─── Chat input ─── */
.stChatInput {
    border-radius: 0px !important;
}
.stChatInput textarea {
    background: rgba(40, 40, 40, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 0px !important;
    color: #e0e0ff !important;
    font-family: 'Inter', sans-serif !important;
}
.stChatInput textarea:focus {
    border-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: none !important;
}

/* ─── Expander (Sources) ─── */
.streamlit-expanderHeader {
    background: rgba(99, 102, 241, 0.08) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(99, 102, 241, 0.15) !important;
    color: #a5b4fc !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
.streamlit-expanderHeader:hover {
    background: rgba(99, 102, 241, 0.15) !important;
}
.streamlit-expanderContent {
    background: rgba(15, 15, 35, 0.6) !important;
    border-radius: 0 0 12px 12px !important;
    border: 1px solid rgba(99, 102, 241, 0.1) !important;
    border-top: none !important;
}

/* ─── Source card ─── */
.source-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.06));
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    transition: all 0.3s ease;
}
.source-card:hover {
    border-color: rgba(99,102,241,0.35);
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.1);
}
.source-card .source-title {
    font-weight: 600;
    color: #a5b4fc;
    font-size: 0.9rem;
    margin-bottom: 4px;
}
.source-card .source-meta {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 6px;
}
.source-card .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 500;
}
.badge-type {
    background: rgba(99,102,241,0.2);
    color: #a5b4fc;
}
.badge-score {
    background: rgba(16,185,129,0.2);
    color: #6ee7b7;
}
.source-card .source-snippet {
    color: #9ca3af;
    font-size: 0.82rem;
    line-height: 1.5;
    margin-top: 6px;
}

/* ─── Slider ─── */
.stSlider > div > div > div {
    background: rgba(99,102,241,0.3) !important;
}

/* ─── Dividers ─── */
hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* ─── Title area ─── */
.main-title {
    text-align: center;
    padding: 0.5rem 0 0.2rem 0;
}
.main-title h1 {
    background: linear-gradient(135deg, #a5b4fc, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0;
}
.main-subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ─── Status pill ─── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}
.status-online {
    background: rgba(16,185,129,0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16,185,129,0.25);
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}

/* ─── Animations ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
}

/* ─── Architecture diagram box ─── */
.arch-box {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 10px;
    padding: 0.8rem;
    margin-top: 0.5rem;
    font-size: 0.78rem;
    color: #9ca3af;
    line-height: 1.8;
}
.arch-box .arrow { color: #6366f1; font-weight: 600; }
.arch-box .node {
    display: inline-block;
    padding: 2px 6px;
    background: rgba(99,102,241,0.12);
    border-radius: 4px;
    color: #a5b4fc;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR — INFO & SETTINGS
# =============================================================================

with st.sidebar:
    st.markdown("## ⚖️ HR & Legal RAG")
    st.caption("Trợ lý hỏi đáp về Luật Lao động, Hợp đồng & Nhân sự")

    # Status indicator
    st.markdown("""
    <div class="status-pill status-online">
        <div class="pulse-dot"></div>
        Hệ thống đang hoạt động
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### ⚙️ Thiết lập tìm kiếm")
    top_k = st.slider("Số lượng tài liệu (top_k)", 3, 10, 5)
    
    doc_type = st.selectbox(
        "Loại tài liệu ưu tiên", 
        ["Tất cả", "Quy định/Chính sách (Legal)", "Tin tức/Hướng dẫn (News)"]
    )
    
    min_score = st.slider("Độ tin cậy tối thiểu (Score)", 0.0, 1.0, 0.3, 0.05)

    st.markdown("#### 🔬 Kỹ thuật RAG")
    rag_mode = st.selectbox(
        "Chọn chiến lược tìm kiếm",
        ["⚡ Cơ bản (Top-K only)", "🔀 Hybrid Search (Semantic + BM25)", "🏆 Hybrid + Rerank (Tối ưu)"],
        index=2,
        help="Kỹ thuật càng cao → câu trả lời càng chính xác và có nguồn trích dẫn rõ ràng hơn"
    )
    # Hiện mô tả ngắn bên dưới
    mode_desc = {
        "⚡ Cơ bản (Top-K only)": "🟡 Tìm theo từ khóa đơn giản, không sắp xếp lại kết quả.",
        "🔀 Hybrid Search (Semantic + BM25)": "🟠 Kết hợp tìm kiếm ngữ nghĩa + từ khóa BM25, bao phủ rộng hơn.",
        "🏆 Hybrid + Rerank (Tối ưu)": "🟢 Sắp xếp lại kết quả theo mức độ liên quan + trích dẫn nguồn đầy đủ.",
    }
    st.caption(mode_desc[rag_mode])

    st.divider()

    st.markdown("#### 💡 Câu hỏi gợi ý")
    suggestions = [
        "Tiền lương làm thêm giờ vào ngày lễ được tính như thế nào?",
        "Thời gian thử việc tối đa đối với người quản lý doanh nghiệp là bao lâu?",
        "Doanh nghiệp có được sa thải nhân viên nữ vì lý do kết hôn không?",
        "Hợp đồng lao động 1 tháng có bắt buộc phải đóng Bảo hiểm Xã hội không?",
        "Người lao động được nghỉ bao nhiêu ngày phép năm nếu làm đủ 12 tháng?",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True, key=f"sug_{s[:20]}"):
            st.session_state["pending_query"] = s

# =============================================================================
# SESSION STATE
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# =============================================================================
# MAIN CHAT AREA
# =============================================================================

# Title with gradient
st.markdown("""
<div class="main-title">
    <h1>⚖️ HR & Legal RAG Chatbot</h1>
</div>
<div class="main-subtitle">
    Hệ thống hỏi đáp thông minh về Nhân sự & Pháp lý — Bộ luật Lao động · Hợp đồng · BHXH
</div>
""", unsafe_allow_html=True)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
            with st.expander(f"📚 Nguồn tham khảo ({len(msg['sources'])} tài liệu)"):
                for i, src in enumerate(msg["sources"], 1):
                    meta = src.get("metadata", {})
                    source_name = meta.get("source", "Unknown")
                    doc_type = meta.get("type", "unknown")
                    score = src.get("score", 0)
                    snippet = src.get("content", "")[:250].replace("\n", " ")

                    # Determine score color
                    score_color = "#6ee7b7" if score >= 0.8 else "#fbbf24" if score >= 0.5 else "#f87171"

                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-title">📄 [{i}] {source_name}</div>
                        <div class="source-meta">
                            <span class="badge badge-type">{doc_type}</span>
                            <span class="badge badge-score" style="color: {score_color}">
                                ⚡ {score:.4f}
                            </span>
                        </div>
                        <div class="source-snippet">{snippet}…</div>
                    </div>
                    """, unsafe_allow_html=True)

# =============================================================================
# QUERY HANDLING
# =============================================================================

# Xử lý khi bấm nút gợi ý hoặc nhập câu hỏi mới
user_input = st.chat_input("Nhập câu hỏi của bạn về Luật Lao động, Hợp đồng, BHXH...")
query = user_input or st.session_state.pending_query

if query:
    st.session_state.pending_query = None

    # Hiển thị câu hỏi của user
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Sinh câu trả lời từ RAG Pipeline
    spinner_msg = {
        "⚡ Cơ bản (Top-K only)": "⚡ Đang tìm kiếm cơ bản...",
        "🔀 Hybrid Search (Semantic + BM25)": "🔀 Đang chạy Hybrid Search...",
        "🏆 Hybrid + Rerank (Tối ưu)": "🏆 Đang Rerank và tổng hợp câu trả lời tối ưu...",
    }.get(rag_mode, "🔍 Đang tìm kiếm...")

    with st.chat_message("assistant"):
        with st.spinner(spinner_msg):
            try:
                # Truyền lịch sử chat vào để LLM có context hội thoại
                chat_history = st.session_state.messages[:-1]  # Bỏ tin nhắn user vừa gửi
                response = generate_with_citation(
                    query, 
                    top_k=top_k, 
                    chat_history=chat_history,
                    min_score=min_score,
                    doc_type=doc_type,
                    rag_mode=rag_mode
                )

                answer = response.get("answer", "Chưa thể trả lời.")
                sources = response.get("sources", [])

            except NotImplementedError:
                answer = "⚠️ **Task 10 chưa được implement.** Hãy hoàn thành `src/task10_generation.py` để kết nối pipeline vào UI!"
                sources = []
            except Exception as e:
                answer = f"❌ **Lỗi khi chạy RAG Pipeline:** {e}"
                sources = []

            st.markdown(answer)

            if sources:
                with st.expander(f"📚 Nguồn tham khảo ({len(sources)} tài liệu)"):
                    for i, src in enumerate(sources, 1):
                        meta = src.get("metadata", {})
                        source_name = meta.get("source", "Unknown")
                        doc_type = meta.get("type", "unknown")
                        score = src.get("score", 0)
                        snippet = src.get("content", "")[:250].replace("\n", " ")

                        score_color = "#6ee7b7" if score >= 0.8 else "#fbbf24" if score >= 0.5 else "#f87171"

                        st.markdown(f"""
                        <div class="source-card">
                            <div class="source-title">📄 [{i}] {source_name}</div>
                            <div class="source-meta">
                                <span class="badge badge-type">{doc_type}</span>
                                <span class="badge badge-score" style="color: {score_color}">
                                    ⚡ {score:.4f}
                                </span>
                            </div>
                            <div class="source-snippet">{snippet}…</div>
                        </div>
                        """, unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
