# Pengujian

Jalankan dari root repo: `pytest tests/`

| File | Menguji | Status |
|---|---|---|
| `test_ingest.py` | Modul 1: chunking dan loader | ada, offline |
| `test_router.py` | Modul 4: router, `is_ready`, `status` | ada, offline |
| `test_tfidf.py` | Modul 2 | kosong |
| `test_rag_guard.py` | Modul 3: guard relevansi, flag grounded (11 tes, juga bisa `python -m unittest discover -s tests`) | ada, offline |
| `kalibrasi_threshold.py` | memilih `RAG_MAX_DISTANCE`: `python -m tests.kalibrasi_threshold` (butuh hasil ingest) | ada |
| `pertanyaan_uji.csv` | kolom `pertanyaan, seharusnya_ada (ya/tidak), keterangan`; masih berisi CONTOH, ganti dengan pertanyaan nyata | bahan tabel pengujian laporan |
