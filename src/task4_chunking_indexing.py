"""
Task 4 — Chunking & Indexing vào Vector Store.

Chủ đề: Luật Lao Động cho Gen Z. Dữ liệu (data/standardized/) gồm:
    - legal/: Bộ luật Lao động 2019, Nghị định 145/2020, 38/2022, hợp đồng mẫu
      — cấu trúc rõ theo Markdown heading (# CHƯƠNG, ## /### Điều).
    - news/: bài viết diễn giải luật cho người trẻ — heading phẳng hơn (## mục).

Chunking strategy: RecursiveCharacterTextSplitter với separators ưu tiên tách
tại ranh giới heading (### Điều, ## mục, # chương) trước, chỉ rơi xuống tách
theo đoạn/câu khi 1 khối vẫn vượt CHUNK_SIZE. Chọn cách này thay vì
MarkdownHeaderTextSplitter thuần vì MarkdownHeaderTextSplitter không đảm bảo
giới hạn kích thước chunk (1 Điều dài vẫn ra 1 chunk to) — recursive splitter
vừa tôn trọng ranh giới ngữ nghĩa (Điều luật) vừa đảm bảo chunk không vượt size.

Embedding model: Jina Embeddings v3 (API, "jina-embeddings-v3") — multilingual,
tốt cho tiếng Việt pháp lý. Dùng qua API thay vì tải model local (BAAI/bge-m3,
~2.2GB) vì mạng không ổn định để tải file lớn; API tránh hoàn toàn vấn đề này
và hỗ trợ sẵn task-specific embedding (retrieval.passage cho index,
retrieval.query cho query) giúp tăng chất lượng retrieval.

Vector Store: ChromaDB — local, persistent, không cần Docker.

Cài đặt:
    pip install langchain-text-splitters chromadb requests python-dotenv

Cần JINA_API_KEY trong .env (đăng ký tại https://jina.ai).

Lưu ý quan trọng: nếu sau này đổi corpus (đổi chủ đề, thêm/bớt tài liệu), phải XÓA
chroma_db/ cũ trước khi reindex — nếu không, chunk cũ và mới sẽ tồn tại lẫn lộn
trong cùng collection, retrieval sẽ trả về kết quả rác từ dữ liệu cũ.
"""

import os
from functools import lru_cache
from pathlib import Path

import chromadb
import requests
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"


# =============================================================================
# CONFIGURATION
# =============================================================================

# CHUNK_SIZE=500: đủ chứa trọn 1 Điều luật ngắn/trung bình (phần lớn Điều trong
# Bộ luật Lao động dài 200-800 ký tự) mà không nhồi nhiều Điều không liên quan
# vào cùng 1 chunk.
# CHUNK_OVERLAP=75 (15%): giữ ngữ cảnh câu dẫn/khoản liền kề khi 1 Điều dài bị
# cắt thành nhiều chunk (văn bản luật hay tham chiếu "khoản 1 Điều này").
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75
CHUNKING_METHOD = "recursive"  # "recursive" | "markdown_header" | "semantic"

# jina-embeddings-v3 (API): multilingual, tốt cho tiếng Việt pháp lý, dimension
# 1024 (Matryoshka — có thể truncate nhỏ hơn nếu cần nhưng giữ mặc định).
EMBEDDING_MODEL = "jina-embeddings-v3"
EMBEDDING_DIM = 1024
JINA_EMBEDDINGS_URL = "https://api.jina.ai/v1/embeddings"

VECTOR_STORE = "chromadb"
COLLECTION_NAME = "labor_law_docs"


# =============================================================================
# SHARED HELPERS (dùng chung với Task 5)
# =============================================================================

def embed_texts(texts: list[str], task: str) -> list[list[float]]:
    """
    Gọi Jina Embeddings API (jina-embeddings-v3).

    Args:
        texts: danh sách văn bản cần embed
        task: "retrieval.passage" khi embed chunk để index (Task 4),
              "retrieval.query" khi embed câu hỏi để search (Task 5) —
              Jina v3 dùng LoRA adapter riêng cho từng loại, tăng chất lượng
              retrieval so với dùng chung 1 kiểu embedding.

    Returns:
        List embedding vectors, đúng thứ tự với `texts`.
    """
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        raise RuntimeError("Thiếu JINA_API_KEY trong .env")

    response = requests.post(
        JINA_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": EMBEDDING_MODEL,
            "task": task,
            "dimensions": EMBEDDING_DIM,
            "input": texts,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = sorted(response.json()["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in data]


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.ClientAPI:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    documents = []
    for md_file in sorted(STANDARDIZED_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if not content:
            continue
        doc_type = "legal" if "legal" in md_file.parts else "news"
        documents.append({
            "content": content,
            "metadata": {"source": md_file.name, "type": doc_type},
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents theo RecursiveCharacterTextSplitter, ưu tiên tách tại
    ranh giới heading Markdown (Điều/mục/chương) trước khi rơi xuống đoạn/câu.

    Returns:
        List of {'content': str, 'metadata': dict} — mỗi item là 1 chunk
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n### ", "\n## ", "\n# ", "\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            chunks.append({
                "content": chunk_text,
                "metadata": {**doc["metadata"], "chunk_index": i},
            })
    return chunks


def embed_chunks(chunks: list[dict], batch_size: int = 32) -> list[dict]:
    """
    Embed toàn bộ chunks qua Jina API (task="retrieval.passage").

    Returns:
        Mỗi chunk dict được thêm key 'embedding': list[float]
    """
    texts = [c["content"] for c in chunks]
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings.extend(embed_texts(batch, task="retrieval.passage"))

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb
    return chunks


def index_to_vectorstore(chunks: list[dict]):
    """Lưu chunks vào ChromaDB (upsert theo id ổn định = source + chunk_index)."""
    collection = get_collection()

    ids = [f"{c['metadata']['source']}_chunk_{c['metadata']['chunk_index']}" for c in chunks]
    collection.upsert(
        ids=ids,
        documents=[c["content"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE} (collection={COLLECTION_NAME})")
    print("=" * 50)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"✓ Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("✓ Indexed to vector store")


if __name__ == "__main__":
    run_pipeline()
