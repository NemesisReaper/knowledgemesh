import unittest

from packages.search import (
    DocumentRecord, SearchIndex, BM25Ranker, SemanticIndex,
    HybridSearcher, RetrievalService, cosine_similarity,
)


class TinyEncoder:
    def encode(self, texts):
        # Deliberately tiny deterministic test encoder.
        vocab = ("agent", "knowledge", "security", "evidence")
        return [[float(text.casefold().count(word)) for word in vocab] for text in texts]


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.index = SearchIndex()
        self.index.upsert_many([
            DocumentRecord(id="a", title="Agent knowledge", content="Evidence for agents."),
            DocumentRecord(id="b", title="Security", content="Security controls and audit."),
            DocumentRecord(id="c", title="Knowledge graph", content="Knowledge discovery for agents."),
        ])

    def test_bm25_ranking(self):
        hits = BM25Ranker(self.index).search("agent knowledge")
        self.assertTrue(hits)
        self.assertEqual(hits[0].document.id, "a")

    def test_upsert_and_remove(self):
        self.index.upsert(DocumentRecord(id="a", title="Updated", content="new material"))
        self.assertEqual(self.index.get("a").title, "Updated")
        self.assertNotIn("a", [h.document.id for h in BM25Ranker(self.index).search("agent")])
        self.assertTrue(self.index.remove("a"))
        self.assertIsNone(self.index.get("a"))

    def test_semantic_and_hybrid(self):
        semantic = SemanticIndex(TinyEncoder())
        semantic.index(list(self.index.documents()))
        self.assertTrue(semantic.search("agent knowledge"))
        self.assertTrue(HybridSearcher(self.index, semantic).search("agent knowledge"))

    def test_retrieval_is_bounded(self):
        result = RetrievalService(self.index).retrieve("knowledge", max_chars=20)
        self.assertLessEqual(len(result.context), 20)
        self.assertTrue(result.document_ids)

    def test_cosine(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [1, 0]), 1.0)


if __name__ == "__main__":
    unittest.main()
