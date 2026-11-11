"""Hybrid lexical/semantic search with reciprocal-rank fusion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .indexing import SearchIndex
from .ranking import BM25Ranker, SearchHit
from .semantic import SemanticIndex


@dataclass(frozen=True, slots=True)
class HybridSearchConfig:
    lexical_weight: float = 1.0
    semantic_weight: float = 1.0
    rrf_k: int = 60
    candidate_multiplier: int = 3

    def __post_init__(self) -> None:
        if self.lexical_weight < 0 or self.semantic_weight < 0:
            raise ValueError("weights cannot be negative")
        if self.lexical_weight == 0 and self.semantic_weight == 0:
            raise ValueError("at least one search weight must be positive")
        if self.rrf_k < 1 or self.candidate_multiplier < 1:
            raise ValueError("rrf_k and candidate_multiplier must be >= 1")


def reciprocal_rank_fusion(
    result_sets: list[list[SearchHit]], *, k: int = 60,
    weights: list[float] | None = None, limit: int = 10,
) -> list[SearchHit]:
    if k < 1 or limit < 1:
        raise ValueError("k and limit must be >= 1")
    if weights is None:
        weights = [1.0] * len(result_sets)
    if len(weights) != len(result_sets) or any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative and match result sets")
    docs = {}
    scores: dict[str, float] = {}
    origins: dict[str, list[str]] = {}
    for result_set, weight in zip(result_sets, weights):
        for rank, hit in enumerate(result_set, 1):
            doc_id = hit.document.id
            docs[doc_id] = hit.document
            scores[doc_id] = scores.get(doc_id, 0.0) + weight / (k + rank)
            origins.setdefault(doc_id, []).append(hit.source)
    ordered = sorted(scores, key=lambda key: (-scores[key], key))[:limit]
    return [SearchHit(docs[key], scores[key], rank, "hybrid",
                      {"sources": sorted(set(origins[key]))})
            for rank, key in enumerate(ordered, 1)]


class HybridSearcher:
    def __init__(self, index: SearchIndex, semantic_index: SemanticIndex | None = None,
                 config: HybridSearchConfig | None = None) -> None:
        self.lexical = BM25Ranker(index)
        self.semantic = semantic_index
        self.config = config or HybridSearchConfig()

    def search(self, query: str, *, limit: int = 10,
               filters: Mapping[str, Any] | None = None) -> list[SearchHit]:
        candidate_limit = limit * self.config.candidate_multiplier
        sets: list[list[SearchHit]] = []
        weights: list[float] = []
        if self.config.lexical_weight:
            sets.append(self.lexical.search(query, limit=candidate_limit, filters=filters))
            weights.append(self.config.lexical_weight)
        if self.semantic is not None and self.config.semantic_weight:
            semantic_hits = self.semantic.search(query, limit=candidate_limit)
            if filters:
                semantic_hits = [hit for hit in semantic_hits if _matches(hit, filters)]
            sets.append(semantic_hits)
            weights.append(self.config.semantic_weight)
        return reciprocal_rank_fusion(sets, k=self.config.rrf_k,
                                      weights=weights, limit=limit)


def _matches(hit: SearchHit, filters: Mapping[str, Any]) -> bool:
    doc = hit.document
    for key, value in filters.items():
        if key == "metadata":
            if not isinstance(value, Mapping) or any(doc.metadata.get(k) != v for k, v in value.items()):
                return False
        elif not hasattr(doc, key) or getattr(doc, key) != value:
            return False
    return True
