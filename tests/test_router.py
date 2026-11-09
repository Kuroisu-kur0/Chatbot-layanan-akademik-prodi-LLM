"""Uji Modul 4 (router). Pipeline ditiru, jadi tidak butuh Chroma maupun API key."""
from backend import router
from backend.rag import settings


def test_route_menandai_via_rag_dan_meneruskan_field(monkeypatch):
    monkeypatch.setattr(router, "answer_with_rag", lambda q: {
        "answer": "x", "sources": ["a.md"], "grounded": True,
        "reason": "ok", "llm_called": True})
    hasil = router.route("tes")
    assert hasil["via"] == "rag"
    assert hasil["grounded"] is True and hasil["sources"] == ["a.md"]


def test_is_ready_mengikuti_api_key(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    assert router.is_ready() is False
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "kunci")
    assert router.is_ready() is True


def test_status_memuat_jumlah_dokumen(monkeypatch):
    class Koleksi:
        def count(self):
            return 7

    monkeypatch.setattr(router, "get_collection", lambda: Koleksi())
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "kunci")
    assert router.status() == {"status": "ok", "gemini_configured": True, "documents": 7}
