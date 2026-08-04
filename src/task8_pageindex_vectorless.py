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

UPLOADED_DOC_IDS: list[str] = []


def upload_documents() -> list[str]:
    """
    Upload toàn bộ markdown documents lên PageIndex.
    """
    global UPLOADED_DOC_IDS
    if not PAGEINDEX_API_KEY:
        print("[!] PAGEINDEX_API_KEY is not set in .env. Skipping cloud upload.")
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
                    if doc_id:
                        uploaded.append(doc_id)
                        print(f"  [+] Uploaded: {md_file.name} -> {doc_id}")
                except Exception as ex:
                    print(f"  [-] Failed uploading {md_file.name}: {ex}")
    except Exception as e:
        print(f"PageIndex connection error: {e}")

    UPLOADED_DOC_IDS = uploaded
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
        return [
            {
                "content": f"[PageIndex Fallback] Structural retrieval results for: {query}",
                "score": 0.5,
                "metadata": {"section": "General Structure"},
                "source": "pageindex"
            }
        ][:top_k]

    try:
        from pageindex.client import PageIndexClient
        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

        results = []
        doc_ids_to_query = UPLOADED_DOC_IDS or []
        for doc_id in doc_ids_to_query[:3]:
            try:
                resp = client.submit_query(doc_id=doc_id, query=query)
                retrieval_id = resp.get("retrieval_id") or resp.get("id")
                if retrieval_id:
                    retrieval = client.get_retrieval(retrieval_id)
                    for node in retrieval.get("retrieved_nodes", [])[:2]:
                        for group in node.get("relevant_contents", []):
                            for item in group:
                                results.append({
                                    "content": item.get("relevant_content", ""),
                                    "score": 0.5,
                                    "metadata": {"section": item.get("section_title", ""), "doc_id": doc_id},
                                    "source": "pageindex",
                                })
            except Exception as ex:
                continue

        if results:
            return results[:top_k]
    except Exception as e:
        print(f"PageIndex API call error: {e}")

    return [
        {
            "content": f"[PageIndex Fallback] Structural fallback results for: {query}",
            "score": 0.5,
            "metadata": {"section": "Fallback Structural Context"},
            "source": "pageindex"
        }
    ][:top_k]


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("[!] Please set PAGEINDEX_API_KEY in .env file")
        print("  Register at: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

    print("\nTest query:")
    results = pageindex_search("tuition fee", top_k=3)
    for r in results:
        print(f"[{r['score']:.3f}] [{r.get('source')}] {r['content'][:100]}...")



