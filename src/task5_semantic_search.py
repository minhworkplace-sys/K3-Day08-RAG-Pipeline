"""
Task 5 — Semantic Search Module (+ HyDE bonus).

Dense retrieval trên ChromaDB collection đã index ở Task 4. Dùng chung Jina
Embeddings API + collection với Task 4 (qua embed_texts()/get_collection())
để đảm bảo query vector cùng không gian với vector đã index. Query dùng
task="retrieval.query" (khác "retrieval.passage" lúc index) theo đúng cách
Jina v3 khuyến nghị cho bài toán retrieval.

HyDE (Hypothetical Document Embeddings — Gao et al., 2022): thay vì embed
thẳng câu hỏi ngắn, dùng LLM sinh ra 1 đoạn văn giả định trả lời câu hỏi đó
(văn phong giống văn bản luật/tư vấn pháp lý — giống các chunk thật trong
corpus), rồi embed đoạn văn giả định đó để tìm kiếm. Lý do hiệu quả: câu hỏi
người dùng thường ngắn, khác văn phong với văn bản luật dài — "đoạn trả lời
giả định" nằm gần các chunk thật hơn trong không gian embedding so với câu
hỏi gốc, đặc biệt hữu ích với câu hỏi tình huống đời thường (không dùng đúng
thuật ngữ pháp lý) như "sa thải qua Zalo có đúng luật không".
Lưu ý: đoạn văn giả định CHỈ dùng để tạo vector tìm kiếm, KHÔNG dùng để trả
lời người dùng (có thể sai thông tin vì LLM bịa) — retrieval vẫn trả về
chunk THẬT từ vector store.
"""

from .llm_client import get_llm_client
from .task4_chunking_indexing import embed_texts, get_collection


def _query_to_results(query_vector: list[float], top_k: int) -> list[dict]:
    """Query ChromaDB bằng 1 vector có sẵn, format kết quả đúng chuẩn Task 5."""
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    output = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        # ChromaDB trả cosine distance = 1 - cosine similarity (khi space="cosine")
        score = max(0.0, 1.0 - dist)
        output.append({"content": doc, "score": round(score, 4), "metadata": meta})

    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:top_k]


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score, thang [0, 1]
            'metadata': dict     # source, type, chunk_index
        }
        Sorted by score descending.
    """
    query_vector = embed_texts([query], task="retrieval.query")[0]
    return _query_to_results(query_vector, top_k)


# =============================================================================
# BONUS — HyDE (Hypothetical Document Embeddings)
# =============================================================================

HYDE_PROMPT = """Bạn là chuyên gia tư vấn luật lao động Việt Nam. Hãy viết một đoạn văn ngắn
(3-5 câu) trả lời câu hỏi dưới đây, văn phong giống văn bản pháp luật/tư vấn pháp lý,
có thể trích dẫn số Điều/Khoản nếu phù hợp. Chỉ viết đoạn trả lời, không giải thích thêm,
không nói "tôi không chắc" hay "cần tham khảo thêm".

Câu hỏi: {query}"""


def generate_hypothetical_document(query: str) -> str:
    """Sinh đoạn văn giả định trả lời `query`, dùng làm input để embed (HyDE)."""
    client, model = get_llm_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": HYDE_PROMPT.format(query=query)}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def semantic_search_hyde(query: str, top_k: int = 10) -> list[dict]:
    """
    Semantic search dùng kỹ thuật HyDE: sinh đoạn văn giả định từ LLM, embed
    đoạn đó (task="retrieval.passage" — coi như 1 document thật, không phải
    query ngắn) rồi tìm kiếm, thay vì embed thẳng câu hỏi gốc.

    Returns: cùng shape với semantic_search().
    """
    hypothetical_doc = generate_hypothetical_document(query)
    query_vector = embed_texts([hypothetical_doc], task="retrieval.passage")[0]
    return _query_to_results(query_vector, top_k)


if __name__ == "__main__":
    test_queries = [
        "Thời gian thử việc tối đa cho vị trí lập trình viên là bao lâu?",
        "Công ty sa thải tôi qua tin nhắn Zalo mà không báo trước 30 ngày thì có đúng luật không?",
        "Làm thêm giờ được trả lương như thế nào?",
    ]
    for q in test_queries:
        print(f"\n{'='*70}\nQ: {q}\n{'='*70}")

        print("-- semantic_search (thường) --")
        for r in semantic_search(q, top_k=3):
            print(f"[{r['score']:.3f}] ({r['metadata']['source']}) {r['content'][:100]}...")

        print("-- semantic_search_hyde --")
        for r in semantic_search_hyde(q, top_k=3):
            print(f"[{r['score']:.3f}] ({r['metadata']['source']}) {r['content'][:100]}...")
