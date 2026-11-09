"""Modul 1: memotong teks menjadi chunk dengan tumpang tindih (overlap)."""
from backend import config
from backend.ingest.preprocess import normalize_whitespace


def chunk_text(text: str, size: int = config.CHUNK_SIZE, overlap: int = config.CHUNK_OVERLAP):
    if overlap >= size:
        raise ValueError("overlap harus lebih kecil dari size")
    text = normalize_whitespace(text)
    start = 0
    while start < len(text):
        yield text[start:start + size]
        start += size - overlap
