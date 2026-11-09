# Chatbot Layanan Akademik Prodi Teknik Informatika

Chatbot berbasis Google Gemini API dengan pendekatan Retrieval-Augmented Generation (RAG).
Backend FastAPI, frontend HTML/CSS/JavaScript, dan ChromaDB sebagai penyimpanan vektor lokal.

Rencana alur: pertanyaan dijawab mesin FAQ (TF-IDF) lebih dulu; kalau skornya rendah,
dialihkan ke RAG. Saat ini baru RAG yang aktif (Modul 2 belum dibuat).

## Peta repo (mulai dari sini)

| Saya ingin ... | Buka |
|---|---|
| Memahami alur dan kontrak antar modul | [docs/arsitektur.md](docs/arsitektur.md) |
| Tahu pembagian tugas dan aturan Git | [docs/panduan-tim.md](docs/panduan-tim.md) |
| Mengerjakan data / ingest (Modul 1) | [backend/ingest/](backend/ingest/README.md) |
| Mengerjakan FAQ TF-IDF (Modul 2) | [backend/tfidf/](backend/tfidf/README.md) |
| Mengerjakan RAG + Gemini (Modul 3) | [backend/rag/](backend/rag/README.md) |
| Mengerjakan API dan router (Modul 4) | [backend/main.py](backend/main.py), [backend/router.py](backend/router.py) |
| Mengerjakan tampilan | [frontend/](frontend/) |
| Menjalankan atau menambah pengujian | [tests/](tests/README.md) |
| Bahan laporan (screenshot, hasil uji) | [docs/laporan/](docs/laporan/README.md) |

## Struktur

```
chatbot-akademik-prodi/
├── README.md                  <- Anda di sini
├── requirements.txt
├── .env.example               <- salin jadi .env
├── .gitignore
│
├── backend/
│   ├── main.py                Modul 4 | route FastAPI (tipis)
│   ├── router.py              Modul 4 | TF-IDF dulu, skor rendah -> RAG
│   ├── config.py              bersama | path, API key, model, ukuran chunk, CORS
│   ├── vectorstore.py         bersama | akses ChromaDB (satu-satunya tempat embedding ditentukan)
│   ├── ingest/                Modul 1 | loaders, preprocess, chunking, run_ingest
│   ├── tfidf/                 Modul 2 | engine.py (belum dibuat)
│   ├── rag/                   Modul 3 | settings, retriever, prompt, llm_client, pipeline
│   └── data/
│       ├── dokumen/           dokumen resmi untuk RAG (+ CONTOH_INFORMASI_PRODI.md)
│       ├── faq/faq.csv        pasangan tanya-jawab untuk TF-IDF
│       └── chroma/            HASIL ingest (di-ignore Git)
│
├── frontend/                  index.html, script.js, style.css
├── tests/                     uji per modul + pertanyaan_uji.csv
└── docs/                      arsitektur, panduan tim, bahan laporan
```

## Persyaratan
- Python 3.10+
- Git
- API key Gemini dari Google AI Studio

## Instalasi Windows (PowerShell)
```powershell
git clone https://github.com/USERNAME/chatbot-akademik-prodi.git
cd chatbot-akademik-prodi

py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
notepad .env
```
Isi `GEMINI_API_KEY` pada `.env`. Jangan pernah mengunggah `.env` ke GitHub.

Semua perintah di bawah dijalankan dari **root repo**, bukan dari dalam folder `backend/`.

## Menambahkan dokumen akademik
Letakkan dokumen resmi berformat PDF, TXT, atau MD di `backend/data/dokumen/`, lalu jalankan:
```powershell
python -m backend.ingest.run_ingest
```
(Dulu: `python backend/ingest.py`. Perintah itu sudah tidak berlaku.)
Dokumen contoh hanya placeholder. Ganti dengan informasi resmi prodi sebelum digunakan.

## Menjalankan backend
```powershell
uvicorn backend.main:app --reload
```
API berjalan di `http://127.0.0.1:8000`. Dokumentasi API: `http://127.0.0.1:8000/docs`.

## Menjalankan frontend
Buka terminal kedua:
```powershell
py -m http.server 5500 --directory frontend
```
Buka `http://127.0.0.1:5500`.

## Menjalankan pengujian
```powershell
pytest tests/
```

## Catatan keamanan dan kualitas
- API key hanya disimpan di `.env`. Kalau sempat ter-push, ganti key-nya; menghapus dari riwayat saja tidak cukup.
- Jangan masukkan data pribadi mahasiswa atau data akademik terbatas ke Knowledge Base publik.
- Batasi akses dokumen dan endpoint ingest untuk penggunaan produksi.
- Jawaban chatbot perlu diverifikasi dan dokumen harus selalu diperbarui.
- Data contoh dalam `backend/data/dokumen` bukan kebijakan resmi kampus.
