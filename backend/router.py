"""Modul 4: menentukan sistem mana yang menjawab.

Rencana: TF-IDF (FAQ) dulu; kalau skor < ambang, alihkan ke RAG.
Saat ini TF-IDF belum ada, jadi semua pertanyaan langsung ke RAG.

Kontrak: lihat docs/arsitektur.md
"""
from backend.rag import settings
from backend.rag.pipeline import answer_with_rag
from backend.rag.retriever import get_collection

# TODO (Modul 4) setelah Modul 2 siap:
# from backend.tfidf.engine import answer as faq_answer
# hasil = faq_answer(question)
# if hasil["score"] >= <ambang TF-IDF>: return {..., "via": "tfidf"}


def is_ready() -> bool:
    """False kalau GEMINI_API_KEY belum diatur."""
    return bool(settings.GEMINI_API_KEY)


def status() -> dict:
    return {"status": "ok", "gemini_configured": is_ready(),
            "documents": get_collection().count()}


def route(question: str) -> dict:
    result = answer_with_rag(question)
    result["via"] = "rag"
    return result
