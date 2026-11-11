"""Optional semantic search interfaces; no embedding model is bundled."""

from __future__ import annotations

import math
from typing import Protocol, Sequence, Mapping, Any

from .indexing import DocumentRecord, SearchIndex
from .ranking import SearchHit


class SemanticEncoder(Protocol):
    """Adapter contract for an embedding model."""
    def encode(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        ...


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have equal dimensions")
    if not left:
        raise ValueError("vectors cannot be empty")
    dot = sum(float(a) * float(b) for a, b in zip(left, right))
    norm_left = math.sqrt(sum(float(a) ** 2 for a in left))
    norm_right = math.sqrt(sum(float(b) ** 2 for b in right))
    if norm_left == 0 or norm_right == 0:
        return 0.0
    return max(-1.0, min(1.0, dot / (norm_left * norm_right)))


class SemanticIndex:
    """In-memory vector index using a caller-provided encoder."""
    def __init__(self, encoder: SemanticEncoder) -> None:
        self.encoder = encoder
        self._vectors: dict[str, tuple[float, ...]] = {}
        self._documents: dict[str, DocumentRecord] = {}

    def index(self, documents: Sequence[DocumentRecord]) -> int:
        if not documents:
            return 0
        vectors = self.encoder.encode([doc.searchable_text for doc in documents])
        if len(vectors) != len(documents):
            raise ValueError("encoder returned a different number of vectors")
        for doc, vector in zip(documents, vectors):
            values = tuple(float(value) for value in vector)
            if not values or any(not math.isfinite(value) for value in values):
                raise ValueError(f"invalid embedding for document {doc.id}")
            self._vectors[doc.id] = values
            self._documents[doc.id] = doc
        return len(documents)

    def remove(self, document_id: str) -> bool:
        existed = self._vectors.pop(document_id, None) is not None
        self._documents.pop(document_id, None)
        return existed

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        vectors = self.encoder.encode([query])
        if len(vectors) != 1:
            raise ValueError("encoder must return one query vector")
        query_vector = tuple(float(value) for value in vectors[0])
        scored = []
        for doc_id, vector in self._vectors.items():
            score = cosine_similarity(query_vector, vector)
            scored.append((doc_id, score))
        scored.sort(key=lambda item: (-item[1], item[0]))
        return [SearchHit(self._documents[key], score, rank, "semantic",
                          {"similarity": score})
                for rank, (key, score) in enumerate(scored[:limit], 1)]
