# Panduan tim

## Pembagian modul

| Modul | Folder / file | Penanggung jawab |
|---|---|---|
| 1. Data dan ingest | `backend/ingest/` | (isi nama) |
| 2. FAQ TF-IDF | `backend/tfidf/` | (isi nama) |
| 3. RAG + Gemini | `backend/rag/` | Alvin |
| 4. API, router, frontend | `backend/main.py`, `backend/router.py`, `frontend/` | (isi nama) |

Aturan utama: kerjakan hanya foldermu sendiri. Mau mengubah folder modul lain, bicarakan dulu.
File bersama (`config.py`, `vectorstore.py`) diubah lewat pull request kecil
yang ditinjau minimal satu orang lain.

## Alur Git

1. Satu orang membuat commit pertama dari kerangka ini, sebelum yang lain mengubah file.
2. Satu branch per modul, misalnya `modul-3-rag`.
3. Gabungkan lewat pull request.
4. Sebelum push: `git pull --rebase origin main`.
5. Jangan pernah commit `.env` atau `backend/data/chroma/`.

## Modul 3 di repo ini

`backend/rag/` sudah berisi Modul 3 versi perbaikan. Tiga penyesuaian titik sambung (isi
logikanya tidak diubah):

1. `rag/settings.py` mengambil path, nama collection, API key, dan nama model dari
   `backend/config.py` (sumber bersama), jadi `.env` selalu dibaca dari root repo.
2. `get_collection()` dan placeholder `get_embedding_function()` pindah ke `backend/vectorstore.py`,
   supaya ingest dan retriever pasti memakai embedding yang sama. `rag/retriever.py` meneruskan ke sana.
3. `main.py` dan `router.py` (Modul 4) memanggil `answer_with_rag()`. Respons API punya field
   `grounded`, `llm_called`, `reason`, dan `via`.

Catatan perilaku: dengan hanya `CONTOH_INFORMASI_PRODI.md`, chatbot akan menolak semua
pertanyaan, karena potongan yang masih berisi `[Isi ...]` sengaja dibuang oleh guard.
Itu normal sampai dokumen resmi dimasukkan.

## Urutan kerja yang disarankan

1. Commit pertama dari repo ini.
2. Modul 1: isi dokumen resmi di `backend/data/dokumen/`, jalankan ingest.
3. Modul 3: isi `tests/pertanyaan_uji.csv` dengan pertanyaan nyata, jalankan
   `python -m tests.kalibrasi_threshold`, lalu set `RAG_MAX_DISTANCE` di `.env`.
4. Modul 3: uji dengan API key asli (`ThinkingConfig`, `HttpOptions(timeout=...)`, retry).
5. Modul 2: isi `backend/data/faq/faq.csv`, buat `tfidf/engine.py`.
6. Modul 4: sambungkan TF-IDF ke `router.route()`.
7. Semua: kumpulkan hasil uji dan screenshot ke `docs/laporan/`.
