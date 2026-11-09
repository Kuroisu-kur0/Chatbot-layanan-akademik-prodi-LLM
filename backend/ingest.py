"""Masukkan dokumen .txt, .md, dan .pdf dari backend/data/dokumen ke ChromaDB."""
from pathlib import Path
import chromadb
from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
DOCS = BASE / "data" / "dokumen"
DB = BASE / "data" / "chroma"
DOCS.mkdir(parents=True, exist_ok=True)
collection = chromadb.PersistentClient(path=str(DB)).get_or_create_collection("dokumen_akademik")

def read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="ignore")

def chunks(text: str, size: int = 900, overlap: int = 120):
    text = " ".join(text.split())
    start = 0
    while start < len(text):
        yield text[start:start + size]
        start += size - overlap

def main():
    documents, ids, metadatas = [], [], []
    for path in DOCS.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".txt", ".md", ".pdf"}:
            content = read_file(path)
            for index, chunk in enumerate(chunks(content)):
                if chunk.strip():
                    ids.append(f"{path.name}-{index}")
                    documents.append(chunk)
                    metadatas.append({"source": path.name, "chunk": index})
    if not documents:
        print("Belum ada dokumen. Tambahkan file PDF/TXT/MD ke backend/data/dokumen.")
        return
    # Reset collection to avoid stale chunks when documents are updated.
    collection = chromadb.PersistentClient(path=str(DB)).get_or_create_collection("dokumen_akademik")
    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Berhasil memasukkan {len(documents)} potongan dokumen.")

if __name__ == "__main__":
    main()
