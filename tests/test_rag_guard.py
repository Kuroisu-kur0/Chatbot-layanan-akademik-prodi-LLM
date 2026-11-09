"""Uji logika Modul 3 tanpa Gemini/Chroma (memakai data tiruan).
Jalankan dari folder root repo:  python -m unittest discover -s tests -v
"""
import unittest

from backend.rag import settings
from backend.rag.pipeline import answer_with_rag
from backend.rag.retriever import filter_relevant, retrieve


def P(text, source="doc.md", distance=0.3):
    return {"text": text, "source": source, "distance": distance}


class LLMPalsu:
    """Mencatat apakah dipanggil, dan mengembalikan jawaban yang sudah ditentukan."""
    def __init__(self, jawaban=None, error=None):
        self.jawaban, self.error, self.dipanggil, self.user_prompt = jawaban, error, 0, ""

    def __call__(self, system, user):
        self.dipanggil += 1
        self.user_prompt = user
        if self.error:
            raise self.error
        return self.jawaban


class TestGuard(unittest.TestCase):
    def test_tanpa_hasil_llm_tidak_dipanggil(self):
        llm = LLMPalsu("apa pun")
        r = answer_with_rag("jam buka perpustakaan?", retriever=lambda q: [], llm=llm)
        self.assertEqual(llm.dipanggil, 0)
        self.assertFalse(r["grounded"]); self.assertEqual(r["reason"], "no_context")
        self.assertEqual(r["answer"], settings.REFUSAL); self.assertEqual(r["sources"], [])

    def test_potongan_terlalu_jauh_dibuang(self):
        llm = LLMPalsu("apa pun")
        jauh = [P("teks tidak nyambung", distance=settings.MAX_DISTANCE + 0.5)]
        r = answer_with_rag("pertanyaan jebakan", retriever=lambda q: jauh, llm=llm)
        self.assertEqual(llm.dipanggil, 0); self.assertFalse(r["grounded"])

    def test_placeholder_isi_tidak_dipakai(self):
        p = [P("Kontak admin prodi: [Isi email/nomor/tautan resmi]")]
        self.assertEqual(filter_relevant(p), [])

    def test_konteks_relevan_memanggil_llm_dan_memberi_sumber(self):
        llm = LLMPalsu("Syarat skripsi minimal 120 SKS [1].")
        r = answer_with_rag("syarat skripsi?", llm=llm,
                            retriever=lambda q: [P("Syarat skripsi 120 SKS.", "pedoman.md")])
        self.assertEqual(llm.dipanggil, 1); self.assertTrue(r["grounded"])
        self.assertEqual(r["sources"], ["pedoman.md"])
        self.assertNotIn("[1]", r["answer"])
        self.assertEqual(r["answer"], "Syarat skripsi minimal 120 SKS.")

    def test_sumber_hanya_yang_dikutip(self):
        llm = LLMPalsu("Jawabannya ada di sini [2].")
        ps = [P("a", "satu.md"), P("b", "dua.md")]
        r = answer_with_rag("q", retriever=lambda q: ps, llm=llm)
        self.assertEqual(r["sources"], ["dua.md"])

    def test_llm_menolak_maka_tidak_grounded_dan_tanpa_sumber(self):
        llm = LLMPalsu(settings.REFUSAL)
        r = answer_with_rag("q", retriever=lambda q: [P("x")], llm=llm)
        self.assertFalse(r["grounded"]); self.assertEqual(r["sources"], [])
        self.assertEqual(r["reason"], "llm_refused")

    def test_llm_error_tidak_menyebar(self):
        llm = LLMPalsu(error=RuntimeError("timeout"))
        r = answer_with_rag("q", retriever=lambda q: [P("x")], llm=llm)
        self.assertEqual(r["reason"], "llm_error"); self.assertFalse(r["grounded"])
        self.assertEqual(r["answer"], settings.ERROR_ANSWER)

    def test_llm_jawaban_kosong(self):
        llm = LLMPalsu(None)
        r = answer_with_rag("q", retriever=lambda q: [P("x")], llm=llm)
        self.assertEqual(r["reason"], "llm_empty")

    def test_prompt_memuat_aturan_dan_konteks(self):
        llm = LLMPalsu("ok [1]")
        answer_with_rag("pertanyaan saya", retriever=lambda q: [P("isi dokumen")], llm=llm)
        self.assertIn("isi dokumen", llm.user_prompt)
        self.assertIn("pertanyaan saya", llm.user_prompt)


class KoleksiPalsu:
    def __init__(self, n): self.n = n
    def count(self): return self.n
    def query(self, query_texts, n_results, include):
        return {"documents": [["d1", "d2"][:n_results]],
                "metadatas": [[{"source": "a.md"}, None][:n_results]],
                "distances": [[0.2, 0.9][:n_results]]}


class TestRetriever(unittest.TestCase):
    def test_koleksi_kosong(self):
        self.assertEqual(retrieve("q", collection=KoleksiPalsu(0)), [])

    def test_format_hasil(self):
        h = retrieve("q", k=2, collection=KoleksiPalsu(5))
        self.assertEqual(h[0], {"text": "d1", "source": "a.md", "distance": 0.2})
        self.assertEqual(h[1]["source"], "Dokumen akademik")


if __name__ == "__main__":
    unittest.main()
