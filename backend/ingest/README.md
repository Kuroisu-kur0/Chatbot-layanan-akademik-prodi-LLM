# Modul 1: Data dan knowledge base

Membaca dokumen resmi, merapikan, memotong menjadi chunk, lalu menyimpannya ke Chroma.

| File | Isi |
|---|---|
| `loaders.py` | `read_file()` (PDF/TXT/MD) dan `iter_document_paths()` |
| `preprocess.py` | `normalize_whitespace()`; tempat stopword/stemming kalau diperlukan (hanya untuk TF-IDF) |
| `chunking.py` | `chunk_text()` (ukuran dan overlap dari `config.py`) |
| `run_ingest.py` | skrip yang dijalankan: `python -m backend.ingest.run_ingest` |

Perilaku sama dengan `ingest.py` asli: collection dikosongkan lalu diisi ulang setiap dijalankan.
Satu perbaikan kecil: id chunk memakai path relatif, jadi dua file bernama sama di subfolder
berbeda tidak lagi bentrok.

Kalau fungsi embedding diganti di `backend/vectorstore.py`, jalankan ulang ingest.
