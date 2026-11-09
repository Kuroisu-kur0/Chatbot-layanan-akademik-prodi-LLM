# Arsitektur dan kontrak antarmuka

Kontrak "API" di bawah sesuai kode yang berjalan sekarang. Kontrak antar modul
(Modul 2 dan 3) adalah usulan; ubah bersama tim kalau perlu, lalu perbarui dokumen ini.

## Alur

```
Frontend  --POST /api/chat {"message"}-->  main.py
                                              |
                                              v
                                        router.route()
                                          |
        (belum ada) tfidf.engine.answer() |--- skor >= ambang --> jawaban FAQ  (via="tfidf")
                                          |
                                          '--- skor rendah ----> rag.pipeline.answer_with_rag()  (via="rag")
                                                                   |-- retriever.retrieve() + filter_relevant()
                                                                   |-- tanpa konteks relevan -> tolak, LLM TIDAK dipanggil
                                                                   '-- prompt + llm_client.generate()  (Gemini)
```

## API HTTP (Modul 4, sudah berjalan)

`GET /api/health` -> `{"status": "ok", "gemini_configured": bool, "documents": int}`

`POST /api/chat`
- Body: `{"message": str}` (2 sampai 2000 karakter)
- Respons 200: `{"answer": str, "sources": [str], "via": str|null, "grounded": bool|null, "llm_called": bool|null, "reason": str|null}`
  - `reason`: `no_context` | `llm_refused` | `llm_error` | `llm_empty` | `ok`
  - Kegagalan Gemini (`llm_error`) kini TIDAK menjadi error HTTP: respons tetap 200 dengan
    kalimat "layanan sedang bermasalah" dan `grounded=false`. Pantau lewat field `reason`.
- 503: `GEMINI_API_KEY` belum diatur

Frontend (`script.js`) memakai `message`, `answer`, dan `sources`. Jangan ubah nama field
tanpa mengubah frontend.

## Kontrak antar modul

### Modul 1 -> Modul 3: isi ChromaDB
Collection `dokumen_akademik`; tiap dokumen punya metadata `{"source": nama_file, "chunk": nomor}`.
Satu-satunya tempat embedding ditentukan: `backend/vectorstore.py`.

### Modul 2: `backend/tfidf/engine.py` (belum dibuat, usulan)
```python
def answer(question: str) -> dict:
    # {"answer": str, "score": float, "matched_question": str}
```

### Modul 3: `backend/rag/` (kode nyata, sudah diuji)
```python
# pipeline.py  <- satu-satunya pintu masuk untuk modul lain
def answer_with_rag(query, retriever=retrieve, llm=generate) -> dict:
    # {"answer": str, "sources": list[str], "grounded": bool,
    #  "reason": "no_context"|"llm_refused"|"llm_error"|"llm_empty"|"ok", "llm_called": bool}

# retriever.py
def retrieve(query, k=None, collection=None) -> list[dict]   # {"text", "source", "distance"}
def filter_relevant(passages, max_distance=None) -> list[dict]
def get_collection()                                          # meneruskan ke backend/vectorstore.py
```

### Modul 4: `backend/router.py`
```python
def route(question: str) -> dict     # hasil answer_with_rag + {"via": "tfidf" | "rag"}
def is_ready() -> bool               # GEMINI_API_KEY terisi
def status() -> dict                 # isi /api/health
```

## Keputusan yang masih terbuka

- [ ] Fungsi embedding Chroma (`backend/vectorstore.py`); kalau diganti, jalankan ulang ingest
- [ ] Nilai ambang jarak RAG (kalibrasi dengan `tests/kalibrasi_threshold.py`)
- [ ] Nilai ambang skor TF-IDF
- [ ] Dokumen resmi publik atau internal (menentukan boleh di-push atau tidak)
- [ ] Nama model Gemini di `.env.example` (`gemini-3.8-flash` dibawa dari repo asli; pastikan namanya valid di akun kalian)
