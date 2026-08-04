"""
Task 10 — Generation Có Citation.

Hướng dẫn:
    1. Chọn top_k, top_p phù hợp (giải thích lý do)
    2. Sắp xếp lại chunks sau reranking để tránh "lost in the middle"
    3. Inject context vào prompt
    4. Yêu cầu LLM trả lời có citation
    5. Nếu không đủ evidence → "I cannot verify this information"

Gợi ý LLM: OpenRouter có nhiều model gắn hậu tố ":free" không tính phí — xem
https://openrouter.ai/models?max_price=0 — phù hợp nếu chưa có credit trả phí.
Base URL: "https://openrouter.ai/api/v1", dùng chung interface với OpenAI SDK.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from .task9_retrieval_pipeline import retrieve


# =============================================================================
# CONFIGURATION — Giải thích lựa chọn
# =============================================================================

# top_k: Số chunks đưa vào context
# Chọn 5 vì: đủ evidence mà không quá dài gây lost in the middle
TOP_K = 5

# top_p (nucleus sampling): Xác suất tích luỹ cho token generation
# Chọn 0.9 vì: đủ diverse nhưng không quá random
TOP_P = 0.9

# temperature: Độ ngẫu nhiên của output
# Chọn 0.3 vì: RAG cần factual, ít sáng tạo
TEMPERATURE = 0.3

# TODO: Chọn LLM model (OpenRouter model ID)
LLM_MODEL = "gpt-4o-mini"  # Sử dụng trực tiếp model của OpenAI


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """Bạn là trợ lý trả lời câu hỏi về dịch vụ và chính sách đại học
(học phí, học bổng, ký túc xá, thư viện, đăng ký học phần).

Quy tắc bắt buộc:
1. Chỉ sử dụng thông tin từ context được cung cấp — KHÔNG bịa đặt
2. Mỗi khẳng định phải có trích dẫn ngay sau, ví dụ: [Tuition Fees, 2026]
3. Nếu context không đủ thông tin → trả lời: "Tôi không thể xác minh thông tin này từ nguồn hiện có"
4. Trả lời bằng tiếng Việt, có cấu trúc rõ ràng theo đoạn văn
5. Không suy luận hay mở rộng ngoài những gì được nêu trong context"""


# =============================================================================
# DOCUMENT REORDERING (tránh lost in the middle)
# =============================================================================

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sắp xếp chunks để tránh "lost in the middle" effect.

    LLM nhớ tốt thông tin ở ĐẦU và CUỐI prompt, quên thông tin ở GIỮA.
    Strategy: đặt chunks quan trọng nhất ở đầu và cuối, kém quan trọng ở giữa.

    Input order (by score):  [1, 2, 3, 4, 5]
    Output order:            [1, 3, 5, 4, 2]
    (best first, worst in middle, second-best last)

    Args:
        chunks: List sorted by score descending (from retrieval)

    Returns:
        List reordered để maximize LLM attention.
    """
    if len(chunks) <= 2:
        return chunks

    front = chunks[::2]   # Các phần tử ở vị trí 0, 2, 4... sẽ lên đầu
    back = chunks[1::2]   # Các phần tử ở vị trí 1, 3, 5... sẽ được lật ngược và đưa xuống cuối
    return front + back[::-1]


# =============================================================================
# CONTEXT FORMATTING
# =============================================================================

def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thành context string cho prompt.
    Mỗi chunk có label source để LLM có thể cite.

    Args:
        chunks: List of {'content': str, 'metadata': dict, 'score': float}

    Returns:
        Formatted context string.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", f"Source {i}")
        doc_type = chunk.get("metadata", {}).get("type", "unknown")
        context_parts.append(
            f"[Document {i} | Source: {source} | Type: {doc_type}]\n"
            f"{chunk['content']}\n"
        )
    return "\n---\n".join(context_parts)


# =============================================================================
# GENERATION
# =============================================================================

def generate_with_citation(query: str, top_k: int = 5, chat_history: list = None, min_score: float = 0.0, doc_type: str = "Tất cả", rag_mode: str = "🏆 Hybrid + Rerank (Tối ưu)") -> dict:
    """
    End-to-end RAG generation có citation.
    
    Pipeline:
        1. Gọi retrieve(query) lấy top_k chunks
        2. Nếu không có context -> fallback "I cannot answer..."
        3. Sắp xếp lại context (reorder)
        4. Format context thành text
        5. Gọi LLM (OpenAI API qua OpenRouter/OpenAI) trả về JSON
    """
    if chat_history is None:
        chat_history = []
        
    # MOCK DATA: Giả lập hàm retrieve vì Task 9 (Role 4) chưa xong
    # Khi nào Role 4 làm xong, bạn đổi cờ USE_MOCK = False là sẽ chạy thật
    USE_MOCK = True
    
    if USE_MOCK:
        mock_chunks = [
            {
                "content": "Học phí học kỳ 1 năm 2026 tại RMIT là 30 triệu VND. Sinh viên đóng trước hạn được giảm 5%.", 
                "metadata": {"source": "Quy_dinh_hoc_phi.pdf", "year": "2026", "type": "pdf"},
                "score": 0.88
            },
            {
                "content": "Để đặt phòng học nhóm ở thư viện, sinh viên phải dùng app LibraryBooking.", 
                "metadata": {"source": "Huong_dan_thu_vien.pdf", "type": "pdf"},
                "score": 0.75
            },
            {
                "content": "Học bổng Academic Achievement dành cho sinh viên quốc tế giảm 20% học phí.", 
                "metadata": {"source": "Chinh_sach_hoc_bong.pdf", "type": "pdf"},
                "score": 0.65
            }
        ]
        # Lọc Mock Data theo score và type
        chunks = []
        for chunk in mock_chunks:
            if chunk["score"] < min_score:
                continue
            if doc_type == "Quy định/Chính sách (Legal)" and chunk["metadata"].get("type") != "pdf":
                continue
            if doc_type == "Tin tức/Hướng dẫn (News)" and chunk["metadata"].get("type") == "pdf":
                continue
            chunks.append(chunk)
            
        chunks = chunks[:top_k]
    else:
        # Gọi hàm thật khi USE_MOCK = False
        chunks = retrieve(query, top_k=top_k)

    # ── Áp dụng kỹ thuật RAG theo mode được chọn ──────────────────────────
    is_basic  = "Cơ bản"  in rag_mode
    is_hybrid = "Hybrid Search" in rag_mode and "Rerank" not in rag_mode
    is_rerank = "Rerank"  in rag_mode

    if is_basic:
        # Chỉ lấy 1 đoạn đầu tiên, prompt tối giản
        chunks_to_use = chunks[:1]
        system_prompt = "Bạn là trợ lý đại học. Trả lời ngắn gọn dựa vào tài liệu."
    elif is_hybrid:
        # Dùng tất cả chunks, prompt đầy đủ hơn, không sắp xếp lại
        chunks_to_use = chunks
        system_prompt = SYSTEM_PROMPT
    else:  # Hybrid + Rerank (Tối ưu)
        # Sắp xếp lại và dùng toàn bộ prompt tối ưu với citation
        chunks_to_use = reorder_for_llm(chunks)
        system_prompt = SYSTEM_PROMPT

    # Step 3: Format context
    context = format_context(chunks_to_use)

    # Step 4: Build prompt & History
    if is_basic:
        # Prompt đơn giản, không có history
        user_message = f"Tài liệu: {context}\n\nCâu hỏi: {query}"
        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}]
    else:
        user_message = f"""Context:\n{context}\n\n---\n\nQuestion: {query}"""
        messages = [{"role": "system", "content": system_prompt}]
        if chat_history:
            for msg in chat_history[-4:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

    # Step 5: Call LLM (OpenRouter — OpenAI-compatible API)
    from openai import OpenAI
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or "sk-or-placeholder"
    
    # Chỉ gọi API nếu có key thực, nếu không thì trả về kết quả giả để test UI
    if api_key == "sk-or-placeholder":
        answer = f"⚠️ CHÚ Ý: Chưa cấu hình OPENROUTER_API_KEY trong file .env!\n\nĐây là câu trả lời mô phỏng: Dựa vào tài liệu, có vẻ như câu hỏi của bạn là về '{query}'. Tuy nhiên tôi không thể truy vấn thật vì chưa có API Key."
    else:
        try:
            # Nếu dùng key của OpenAI thì bỏ base_url đi
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                temperature=TEMPERATURE,
                top_p=TOP_P,
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Lỗi gọi LLM API: {str(e)}"

    # Step 6: Return
    return {
        "answer": answer,
        "sources": chunks_to_use,
        "retrieval_source": "mock_data" if USE_MOCK else (chunks[0].get("metadata", {}).get("source", "hybrid") if chunks else "none")
    }


if __name__ == "__main__":
    test_queries = [
        "Học phí tại RMIT Vietnam là bao nhiêu?",
        "Làm sao để đặt phòng học nhóm ở thư viện?",
        "Sinh viên quốc tế có những học bổng nào?",
    ]

    for q in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print("=" * 70)
        result = generate_with_citation(q)
        print(f"\nA: {result['answer']}")
        print(f"\n[Sources: {len(result['sources'])} chunks | via {result['retrieval_source']}]")
