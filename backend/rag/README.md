# Modul 3 - Integrasi LLM & RAG

Antarmuka untuk modul lain: `answer_with_rag(query)` di `pipeline.py`
-> `{"answer", "sources", "grounded", "reason", "llm_called"}`.

| File | Tugas |
|---|---|
| `settings.py` | semua pengaturan (env var) dan kalimat baku |
| `retriever.py` | ambil potongan dari Chroma + saring berdasarkan jarak |
| `prompt.py` | template pembatas (hanya dari konteks) |
| `llm_client.py` | panggilan Gemini (timeout, retry) |
| `pipeline.py` | alur utama + guard + penyaringan sumber |

Env var penting: `GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_THINKING_LEVEL`,
`LLM_MAX_OUTPUT_TOKENS`, `RAG_TOP_K`, `RAG_MAX_DISTANCE` (wajib dikalibrasi).

Catatan integrasi repo: path, nama collection, API key, dan nama model diimpor dari
`backend/config.py`; `get_collection()` dan pilihan embedding ada di `backend/vectorstore.py`
(dipakai bersama oleh ingest). Jalankan semua perintah dari root repo.

Uji logika (tanpa API): `python -m unittest discover -s tests -v` atau `pytest tests/`
Kalibrasi threshold (butuh hasil ingest): `python -m tests.kalibrasi_threshold`
