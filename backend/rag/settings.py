"""Pengaturan Modul 3 (RAG). Semua nilai bisa diubah lewat environment variable / file .env.

Path, nama collection, API key, dan nama model berasal dari backend/config.py (sumber bersama),
yang juga memuat file .env dari root repo.
"""
import os

from backend.config import (  # noqa: F401  (diekspor ulang untuk modul rag lain)
    CHROMA_DIR,
    COLLECTION_NAME,
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

# --- Retrieval ---------------------------------------------------------
TOP_K = int(os.getenv("RAG_TOP_K", "4"))
# Potongan dengan jarak LEBIH BESAR dari ini dianggap tidak relevan.
# NILAI AWAL HANYA TEBAKAN -> kalibrasi dulu dengan tests/kalibrasi_threshold.py
MAX_DISTANCE = float(os.getenv("RAG_MAX_DISTANCE", "1.0"))

# --- LLM (Gemini) ------------------------------------------------------
GEMINI_THINKING_LEVEL = os.getenv("GEMINI_THINKING_LEVEL", "low")   # kosongkan untuk default model
MAX_OUTPUT_TOKENS = int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "1500"))
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_TIMEOUT_S = float(os.getenv("LLM_TIMEOUT_S", "20"))
LLM_RETRIES = int(os.getenv("LLM_RETRIES", "1"))                    # percobaan ulang setelah gagal

# --- Kalimat baku ------------------------------------------------------
REFUSAL = "Mohon maaf, informasi tersebut belum tersedia di dokumen akademik kami."
ERROR_ANSWER = "Maaf, layanan jawaban sedang bermasalah. Silakan coba lagi beberapa saat."
