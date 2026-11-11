"""BM25 lexical ranking."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Mapping, Sequence

from .indexing import DocumentRecord, SearchIndex, tokenize


@dataclass(frozen=True, slots=True)
class SearchHit:
    document: DocumentRecord
    score: float
    rank: int = 0
    source: str = "lexical"
    explanation: Mapping[str, Any] = field(default_factory=dict)


class BM25Ranker:
    """Okapi BM25 ranker over a SearchIndex snapshot."""
    def __init__(self, index: SearchIndex, *, k1: float = 1.5, b: float = 0.75) -> None:
        if k1 <= 0:
            raise ValueError("k1 must be > 0")
        if not 0 <= b <= 1:
            raise ValueError("b must be between 0 and 1")
        self.index, self.k1, self.b = index, float(k1), float(b)

    def search(self, query: str, *, limit: int = 10,
               filters: Mapping[str, Any] | None = None) -> list[SearchHit]:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        terms = tokenize(query)
        if not terms:
            return []
        documents, postings, lengths, _ = self.index.snapshot()
        n = len(documents)
        if not n:
            return []
        avgdl = sum(lengths.values()) / max(n, 1)
        by_id = {doc.id: doc for doc in documents}
        scores: dict[str, float] = {}
        matched: dict[str, list[str]] = {}
        for term in set(terms):
            posting = postings.get(term, {})
            df = len(posting)
            if not df:
                continue
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            for doc_id, tf in posting.items():
                doc = by_id[doc_id]
                if not _matches(doc, filters):
                    continue
                dl = lengths.get(doc_id, 0)
                denom = tf + self.k1 * (1 - self.b + self.b * dl / max(avgdl, 1e-12))
                scores[doc_id] = scores.get(doc_id, 0.0) + idf * (tf * (self.k1 + 1)) / denom
                matched.setdefault(doc_id, []).append(term)
        ordered = sorted(scores, key=lambda key: (-scores[key], key))[:limit]
        return [SearchHit(by_id[key], scores[key], i + 1, "lexical",
                          {"matched_terms": sorted(matched.get(key, []))})
                for i, key in enumerate(ordered)]


def _matches(document: DocumentRecord, filters: Mapping[str, Any] | None) -> bool:
    if not filters:
        return True
    for key, expected in filters.items():
        if key == "metadata":
            if not isinstance(expected, Mapping):
                return False
            if any(document.metadata.get(k) != v for k, v in expected.items()):
                return False
        elif not hasattr(document, key) or getattr(document, key) != expected:
            return False
    return True


def rank_bm25(index: SearchIndex, query: str, *, limit: int = 10,
               k1: float = 1.5, b: float = 0.75,
               filters: Mapping[str, Any] | None = None) -> list[SearchHit]:
    return BM25Ranker(index, k1=k1, b=b).search(query, limit=limit, filters=filters)
