"""Akses ke ChromaDB, dipakai bersama oleh ingest (Modul 1) dan retriever (Modul 3).

Satu-satunya tempat fungsi embedding ditentukan. Kalau tim memutuskan mengganti embedding,
ubah get_embedding_function() di sini, lalu jalankan ulang ingest. Kalau tidak, vektor di
database tidak cocok dengan vektor pertanyaan dan hasil pencarian jadi ngawur.
"""
from backend import config


def get_embedding_function():
    """
    PLACEHOLDER (keputusan tim): fungsi embedding.
    None = pakai bawaan Chroma (setahu Modul 3, berbahasa Inggris). Jika diganti dengan
    embedding multibahasa, ingest HARUS memakai fungsi yang sama dan dijalankan ulang.
    """
    return None


def get_collection():
    import chromadb  # diimpor di sini agar tes tidak butuh Chroma
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    kwargs = {}
    ef = get_embedding_function()
    if ef is not None:
        kwargs["embedding_function"] = ef
    return client.get_or_create_collection(config.COLLECTION_NAME, **kwargs)
