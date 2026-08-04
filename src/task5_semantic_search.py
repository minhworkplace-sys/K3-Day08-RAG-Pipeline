"""
Task 5 — Semantic Search Module.

Dense retrieval trên ChromaDB collection đã index ở Task 4. Dùng chung Jina
Embeddings API + collection với Task 4 (qua embed_texts()/get_collection())
để đảm bảo query vector cùng không gian với vector đã index. Query dùng
task="retrieval.query" (khác "retrieval.passage" lúc index) theo đúng cách
Jina v3 khuyến nghị cho bài toán retrieval.
"""

from .task4_chunking_indexing import embed_texts, get_collection


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


if __name__ == "__main__":
    test_queries = [
        "Thời gian thử việc tối đa cho vị trí lập trình viên là bao lâu?",
        "Công ty sa thải tôi qua tin nhắn Zalo mà không báo trước 30 ngày thì có đúng luật không?",
        "Làm thêm giờ được trả lương như thế nào?",
    ]
    for q in test_queries:
        print(f"\n{'='*70}\nQ: {q}\n{'='*70}")
        results = semantic_search(q, top_k=3)
        for r in results:
            print(f"[{r['score']:.3f}] ({r['metadata']['source']}) {r['content'][:120]}...")
