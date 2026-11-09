"""Pengambilan potongan dokumen dari ChromaDB + penyaringan relevansi."""
import re

from . import settings

# Sementara: potongan yang masih berisi isian kosong "[Isi ...]" tidak boleh jadi "fakta".
_PLACEHOLDER = re.compile(r"\[Isi[^\]]*\]", re.IGNORECASE)


def get_collection():
    """Dipindah ke backend/vectorstore.py supaya ingest dan retriever memakai embedding yang sama."""
    from backend.vectorstore import get_collection as _get_collection
    return _get_collection()


def retrieve(query, k=None, collection=None):
    """Kembalikan [{"text", "source", "distance"}] urut dari yang terdekat."""
    k = k or settings.TOP_K
    col = collection or get_collection()
    total = col.count()
    if total == 0:
        return []
    res = col.query(query_texts=[query], n_results=min(k, total),
                    include=["documents", "metadatas", "distances"])
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0]
    hasil = []
    for doc, meta, dist in zip(docs, metas, dists):
        hasil.append({"text": doc,
                      "source": str((meta or {}).get("source", "Dokumen akademik")),
                      "distance": float(dist)})
    return hasil


def filter_relevant(passages, max_distance=None):
    """Buang potongan yang terlalu jauh atau masih berisi placeholder."""
    batas = settings.MAX_DISTANCE if max_distance is None else max_distance
    return [p for p in passages
            if p["distance"] <= batas and not _PLACEHOLDER.search(p["text"])]
