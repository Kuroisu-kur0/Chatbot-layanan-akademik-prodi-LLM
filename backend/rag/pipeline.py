"""Fungsi utama Modul 3, dipanggil oleh router/backend (Modul 4)."""
import logging
import re

from . import settings
from .llm_client import generate
from .prompt import build_system_prompt, build_user_prompt
from .retriever import filter_relevant, retrieve

log = logging.getLogger("rag.pipeline")
_CITATION = re.compile(r"\[(\d+)\]")


def _result(answer, sources, grounded, reason, llm_called):
    return {"answer": answer, "sources": sources, "grounded": grounded,
            "reason": reason, "llm_called": llm_called}


def answer_with_rag(query, retriever=retrieve, llm=generate):
    """
    Hasil: {"answer", "sources", "grounded", "reason", "llm_called"}
    reason: no_context | llm_refused | llm_error | llm_empty | ok
    """
    passages = filter_relevant(retriever(query))

    # GUARD: tanpa konteks relevan, LLM tidak dipanggil sama sekali
    if not passages:
        log.info("tanpa konteks relevan | q=%r", query)
        return _result(settings.REFUSAL, [], False, "no_context", False)

    try:
        raw = llm(build_system_prompt(), build_user_prompt(query, passages))
    except Exception as exc:
        log.error("LLM error: %s | q=%r", type(exc).__name__, query)
        return _result(settings.ERROR_ANSWER, [], False, "llm_error", True)

    if not raw:
        return _result(settings.ERROR_ANSWER, [], False, "llm_empty", True)

    if settings.REFUSAL.lower() in raw.lower():
        log.info("LLM menolak (tidak ada di konteks) | q=%r", query)
        return _result(settings.REFUSAL, [], False, "llm_refused", True)

    # Sumber: hanya potongan yang dikutip model; jika tidak ada kutipan, semua potongan relevan
    dikutip = {int(n) for n in _CITATION.findall(raw)}
    dipakai = [p for i, p in enumerate(passages, 1) if i in dikutip] or passages
    sumber = list(dict.fromkeys(p["source"] for p in dipakai))
    bersih = _CITATION.sub("", raw)
    bersih = re.sub(r"[ \t]+([.,;:!?])", r"\1", re.sub(r"[ \t]{2,}", " ", bersih)).strip()
    return _result(bersih, sumber, True, "ok", True)
