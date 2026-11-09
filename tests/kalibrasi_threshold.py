"""Bantu memilih RAG_MAX_DISTANCE. Syarat: ingest sudah dijalankan dan chromadb terpasang.
Jalankan dari folder root repo:  python -m tests.kalibrasi_threshold
Isi tests/pertanyaan_uji.csv dengan pertanyaan nyata (ya = ada di dokumen, tidak = jebakan).
"""
import csv
from pathlib import Path

from backend.rag.retriever import retrieve

ya, tidak = [], []
with open(Path(__file__).with_name("pertanyaan_uji.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        hasil = retrieve(row["pertanyaan"], k=1)
        jarak = hasil[0]["distance"] if hasil else float("inf")
        (ya if row["seharusnya_ada"].strip().lower() == "ya" else tidak).append(jarak)
        print(f"{jarak:6.3f}  [{row['seharusnya_ada']:>5}]  {row['pertanyaan']}")

if ya and tidak:
    batas_atas, batas_bawah = max(ya), min(tidak)
    print(f"\nJarak terbesar pertanyaan 'ya'   : {batas_atas:.3f}")
    print(f"Jarak terkecil pertanyaan 'tidak': {batas_bawah:.3f}")
    if batas_atas < batas_bawah:
        print(f"Ada celah. Coba RAG_MAX_DISTANCE di antara keduanya, misalnya {(batas_atas + batas_bawah) / 2:.2f}")
    else:
        print("Tidak ada celah bersih: distribusi saling tumpang tindih. "
              "Pertimbangkan embedding lain atau tambah dokumen.")
