from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types
import chromadb
import os
 
# Colokan ke modul TF-IDF (dikerjakan anggota tim lain).
# Kontrak: cari_jawaban(pertanyaan: str) -> (jawaban: str | None, skor: float 0..1)
# Selama modul itu belum ada, stub di bawah membuat semua pertanyaan diteruskan ke LLM.
try:
    from backend.tfidf import cari_jawaban
except ImportError:
    def cari_jawaban(pertanyaan: str):
        return None, 0.0
 
load_dotenv()
app = FastAPI(title="Chatbot Layanan Akademik Prodi", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
DATA_DIR = Path(__file__).resolve().parent / "data"
CHROMA_DIR = DATA_DIR / "chroma"
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection("dokumen_akademik")
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) if os.getenv("GEMINI_API_KEY") else None
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
 
# Skor TF-IDF minimal agar pertanyaan dijawab langsung tanpa memanggil LLM.
TFIDF_THRESHOLD = float(os.getenv("TFIDF_THRESHOLD", "0.6"))
 
class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
 
class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
    route: str = "llm"   # "tfidf" = jawaban dari FAQ, "llm" = diteruskan ke RAG + Gemini
    score: float = 0.0   # skor kemiripan TF-IDF (0..1)
 
@app.get("/api/health")
def health():
    return {"status": "ok", "gemini_configured": gemini is not None,
            "documents": collection.count(), "tfidf_threshold": TFIDF_THRESHOLD}
 
@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    # Tahap 1: cek TF-IDF dulu. Skor tinggi -> jawab langsung dari FAQ.
    jawaban, skor = cari_jawaban(payload.message)
    skor = float(skor or 0.0)
    if jawaban and skor >= TFIDF_THRESHOLD:
        return ChatResponse(answer=jawaban, sources=["FAQ Program Studi"],
                            route="tfidf", score=round(skor, 3))
 
    # Tahap 2: skor rendah -> teruskan ke RAG + LLM.
    if gemini is None:
        raise HTTPException(503, "GEMINI_API_KEY belum diatur pada file .env.")
    results = collection.query(query_texts=[payload.message], n_results=4) if collection.count() else {}
    docs = (results.get("documents") or [[]])[0]
    metas = (results.get("metadatas") or [[]])[0]
    context = "\n\n".join(docs)
    sources = list(dict.fromkeys(
        str(m.get("source", "Dokumen akademik")) for m in metas if m
    ))
    if not context:
        context = "Belum ada dokumen akademik yang dimasukkan ke Knowledge Base."
    prompt = f"""
Anda adalah Chatbot Layanan Akademik Program Studi Teknik Informatika.
Jawab dalam Bahasa Indonesia yang sopan, jelas, dan ringkas.
Gunakan konteks dokumen sebagai sumber utama. Jangan mengarang jadwal,
nama dosen, kebijakan, biaya, atau tanggal. Jika informasi tidak tersedia
di konteks, katakan bahwa informasi belum tersedia dan sarankan mahasiswa
menghubungi admin program studi. Bedakan informasi resmi dari saran umum.
 
KONTEKS DOKUMEN:
{context}
 
PERTANYAAN MAHASISWA:
{payload.message}
"""
    try:
        response = gemini.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=700),
        )
        answer = response.text or "Maaf, belum ada jawaban yang dapat diberikan."
        return ChatResponse(answer=answer, sources=sources, route="llm", score=round(skor, 3))
    except Exception as exc:
        raise HTTPException(502, f"Gagal menghubungi Gemini API: {type(exc).__name__}")
 