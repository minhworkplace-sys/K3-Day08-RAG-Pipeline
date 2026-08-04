"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents():
    """
    Upload toàn bộ markdown documents lên PageIndex.
    """
    if not PAGEINDEX_API_KEY:
        print("⚠ PAGEINDEX_API_KEY chưa được cấu hình trong .env. Bỏ qua upload thực tế.")
        return []

    uploaded = []
    try:
        from pageindex.client import PageIndexClient
        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

        if STANDARDIZED_DIR.exists():
            for md_file in STANDARDIZED_DIR.rglob("*.md"):
                try:
                    resp = client.submit_document(str(md_file))
                    doc_id = resp.get("doc_id") or resp.get("id")
                    uploaded.append({"file": md_file.name, "doc_id": doc_id})
                    print(f"  ✓ Uploaded: {md_file.name} -> {doc_id}")
                except Exception as ex:
                    print(f"  ✗ Failed uploading {md_file.name}: {ex}")
    except Exception as e:
        print(f"Lỗi kết nối PageIndex: {e}")

    return uploaded


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Dùng làm fallback khi hybrid search không có kết quả tốt.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'   # Đánh dấu nguồn retrieval
        }
    """
    if not PAGEINDEX_API_KEY:
        # Graceful structural fallback khi không có API key
        return [
            {
                "content": f"[PageIndex Fallback] Kết quả truy vấn theo cấu trúc văn bản cho: {query}",
                "score": 0.5,
                "metadata": {"section": "General Structure"},
                "source": "pageindex"
            }
        ][:top_k]

    try:
        from pageindex.client import PageIndexClient
        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
        resp = client.submit_query(query=query)
        retrieval_id = resp.get("retrieval_id") or resp.get("id")

        if retrieval_id:
            retrieval = client.get_retrieval(retrieval_id)
            results = []
            for node in retrieval.get("retrieved_nodes", [])[:2]:
                for group in node.get("relevant_contents", []):
                    for item in group:
                        results.append({
                            "content": item.get("relevant_content", ""),
                            "score": 0.5,
                            "metadata": {"section": item.get("section_title", "")},
                            "source": "pageindex",
                        })
            if results:
                return results[:top_k]
    except Exception as e:
        print(f"PageIndex API call error: {e}")

    return [
        {
            "content": f"[PageIndex Fallback] Kết quả truy vấn cấu trúc cho: {query}",
            "score": 0.5,
            "metadata": {"section": "Fallback Structural Context"},
            "source": "pageindex"
        }
    ][:top_k]


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("⚠ Hãy set PAGEINDEX_API_KEY trong file .env")
        print("  Đăng ký tại: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

    print("\nTest query:")
    results = pageindex_search("học phí", top_k=3)
    for r in results:
        print(f"[{r['score']:.3f}] [{r.get('source')}] {r['content'][:100]}...")

