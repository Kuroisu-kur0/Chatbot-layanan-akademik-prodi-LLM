"""Pemanggilan Gemini. Kode ini belum diuji dengan API sungguhan (perlu API key + koneksi)."""
import logging
import time

from . import settings

log = logging.getLogger("rag.llm")
_client = None


class LLMNotConfigured(RuntimeError):
    pass


def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise LLMNotConfigured("GEMINI_API_KEY belum diatur pada file .env")
        from google import genai
        from google.genai import types
        try:   # batas waktu (milidetik); jika versi SDK berbeda, lewati
            http = types.HttpOptions(timeout=int(settings.LLM_TIMEOUT_S * 1000))
            _client = genai.Client(api_key=settings.GEMINI_API_KEY, http_options=http)
        except Exception:
            _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _build_config(system_prompt):
    from google.genai import types
    kwargs = dict(system_instruction=system_prompt,          # aturan dipisah dari input pengguna
                  temperature=settings.TEMPERATURE,
                  max_output_tokens=settings.MAX_OUTPUT_TOKENS)
    if settings.GEMINI_THINKING_LEVEL:
        try:
            kwargs["thinking_config"] = types.ThinkingConfig(
                thinking_level=settings.GEMINI_THINKING_LEVEL)
        except Exception:
            log.warning("thinking_level tidak didukung SDK ini, memakai pengaturan bawaan")
    return types.GenerateContentConfig(**kwargs)


def generate(system_prompt, user_prompt):
    """Kembalikan teks jawaban, atau None jika kosong. Raise exception jika gagal total."""
    client = _get_client()
    config = _build_config(system_prompt)
    percobaan = settings.LLM_RETRIES + 1
    for i in range(percobaan):
        try:
            resp = client.models.generate_content(
                model=settings.GEMINI_MODEL, contents=user_prompt, config=config)
            return (resp.text or "").strip() or None
        except Exception as exc:
            log.warning("Panggilan LLM gagal (percobaan %d/%d): %s", i + 1, percobaan,
                        type(exc).__name__)
            if i == percobaan - 1:
                raise
            time.sleep(1.5 * (i + 1))
