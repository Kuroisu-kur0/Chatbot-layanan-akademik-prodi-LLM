"""Modul 1: masukkan dokumen ke ChromaDB.

Jalankan dari root repo:  python -m backend.ingest.run_ingest
"""
from backend import config
from backend.ingest.chunking import chunk_text
from backend.ingest.loaders import iter_document_paths, read_file
from backend.vectorstore import get_collection


def main():
    config.DOKUMEN_DIR.mkdir(parents=True, exist_ok=True)

    documents, ids, metadatas = [], [], []
    for path in iter_document_paths(config.DOKUMEN_DIR):
        rel = path.relative_to(config.DOKUMEN_DIR).as_posix()
        for index, chunk in enumerate(chunk_text(read_file(path))):
            if chunk.strip():
                # id memakai path relatif agar dua file bernama sama di subfolder berbeda tidak bentrok
                ids.append(f"{rel}-{index}")
                documents.append(chunk)
                metadatas.append({"source": path.name, "chunk": index})

    if not documents:
        print("Belum ada dokumen. Tambahkan file PDF/TXT/MD ke backend/data/dokumen.")
        return

    collection = get_collection()
    # Kosongkan dulu agar tidak tersisa potongan lama saat dokumen diperbarui.
    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Berhasil memasukkan {len(documents)} potongan dokumen.")


if __name__ == "__main__":
    main()
