"""Modul 4: hanya route FastAPI. Logika ada di router.py dan rag/.

Jalankan dari root repo:  uvicorn backend.main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend import config, router

app = FastAPI(title="Chatbot Layanan Akademik Prodi", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
    via: str | None = None          # "rag" (nanti juga "tfidf")
    grounded: bool | None = None    # True hanya kalau jawaban bersandar pada dokumen
    llm_called: bool | None = None
    reason: str | None = None       # no_context | llm_refused | llm_error | llm_empty | ok


@app.get("/api/health")
def health():
    return router.status()


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    if not router.is_ready():
        raise HTTPException(503, "GEMINI_API_KEY belum diatur pada file .env.")
    return ChatResponse(**router.route(payload.message))
