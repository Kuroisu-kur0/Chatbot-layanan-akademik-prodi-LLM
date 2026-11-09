"""Uji Modul 1 (chunking dan loader). Tidak butuh Chroma maupun API key."""
import pytest

from backend.ingest.chunking import chunk_text
from backend.ingest.loaders import iter_document_paths, read_file
from backend.ingest.preprocess import normalize_whitespace


def test_normalize_whitespace():
    assert normalize_whitespace("a  b\n\n c\t d") == "a b c d"


def test_chunk_text_overlap_dan_batas():
    teks = "x" * 2000
    hasil = list(chunk_text(teks, size=900, overlap=120))
    assert [len(c) for c in hasil] == [900, 900, 440]
    # awal chunk ke-2 bergeser size-overlap = 780
    assert hasil[1] == teks[780:1680]


def test_chunk_text_kosong():
    assert list(chunk_text("   \n  ")) == []


def test_chunk_text_overlap_tidak_valid():
    with pytest.raises(ValueError):
        list(chunk_text("abc", size=10, overlap=10))


def test_loader_hanya_format_didukung(tmp_path):
    (tmp_path / "a.md").write_text("isi a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("isi b", encoding="utf-8")
    (tmp_path / "c.docx").write_text("diabaikan", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "d.MD").write_text("isi d", encoding="utf-8")
    nama = [p.name for p in iter_document_paths(tmp_path)]
    assert nama == ["a.md", "b.txt", "d.MD"]
    assert read_file(tmp_path / "a.md") == "isi a"
