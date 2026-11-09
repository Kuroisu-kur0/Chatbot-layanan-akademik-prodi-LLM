"""Modul 1: membaca dokumen .txt, .md, dan .pdf dari backend/data/dokumen/."""
from pathlib import Path

from pypdf import PdfReader

from backend import config


def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_document_paths(root: Path = config.DOKUMEN_DIR):
    """Semua file dokumen yang didukung di bawah `root` (termasuk subfolder), urut nama."""
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in config.SUPPORTED_SUFFIXES:
            yield path
