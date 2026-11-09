"""Modul 1: pembersihan teks.

Saat ini hanya merapikan spasi (sama seperti kode asli).

CATATAN: stopword removal dan stemming kalau ditambahkan hanya untuk mesin TF-IDF (Modul 2).
Jangan diterapkan pada teks yang disimpan ke Chroma dan dikirim ke Gemini sebagai konteks,
karena kalimatnya jadi rusak dan jawaban LLM ikut memburuk.
"""


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())
