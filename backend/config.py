"""Konfigurasi bersama: path, nama collection, kredensial dan model Gemini, ingest, CORS.

Pengaturan khusus RAG (ambang jarak, timeout, retry, thinking level, kalimat baku)
ada di backend/rag/settings.py, yang mengimpor nilai bersama dari file ini.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")

# --- Path data ---------------------------------------------------------------
DATA_DIR = BASE_DIR / "data"
DOKUMEN_DIR = DATA_DIR / "dokumen"
FAQ_PATH = DATA_DIR / "faq" / "faq.csv"
CHROMA_DIR = DATA_DIR / "chroma"
COLLECTION_NAME = "dokumen_akademik"

# --- Gemini ------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# --- Ingest ------------------------------------------------------------------
CHUNK_SIZE = 900
CHUNK_OVERLAP = 120
SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}

# --- API ---------------------------------------------------------------------
CORS_ORIGINS = ["http://127.0.0.1:5500", "http://localhost:5500"]
