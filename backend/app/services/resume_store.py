from functools import lru_cache

import chromadb

from app.config import settings

COLLECTION = "resume_chunks"


@lru_cache
def _client():
    return chromadb.PersistentClient(path=settings.chroma_path)


def chunk_resume(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if len(p) > 20]


def ingest_resume(text: str) -> int:
    """Replace the stored resume with fresh chunks. Returns chunk count."""
    try:
        _client().delete_collection(COLLECTION)
    except Exception:
        pass  # collection did not exist yet
    collection = _client().get_or_create_collection(COLLECTION)
    chunks = chunk_resume(text)
    if chunks:
        collection.add(
            documents=chunks, ids=[f"chunk-{i}" for i in range(len(chunks))]
        )
    return len(chunks)


def resume_count() -> int:
    return _client().get_or_create_collection(COLLECTION).count()


def search_resume(query: str, k: int = 3) -> list[dict]:
    collection = _client().get_or_create_collection(COLLECTION)
    n = min(k, collection.count())
    if n == 0:
        return []
    result = collection.query(query_texts=[query], n_results=n)
    return [
        {"text": doc, "distance": dist}
        for doc, dist in zip(result["documents"][0], result["distances"][0])
    ]