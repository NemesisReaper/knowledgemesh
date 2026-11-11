"""Context retrieval and evidence-preserving result assembly."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .indexing import DocumentRecord, SearchIndex
from .hybrid import HybridSearcher
from .ranking import BM25Ranker, SearchHit


class RetrievalError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    query: str
    hits: tuple[SearchHit, ...]
    context: str
    document_ids: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)


class RetrievalService:
    """Retrieve ranked documents and construct bounded, traceable context.

    This service does not assert that retrieved text is true or safe to execute.
    Callers must treat document content as untrusted data.
    """
    def __init__(self, index: SearchIndex, searcher: HybridSearcher | BM25Ranker | None = None) -> None:
        self.index = index
        self.searcher = searcher or BM25Ranker(index)

    def retrieve(self, query: str, *, limit: int = 5, max_chars: int = 12000,
                 filters: Mapping[str, Any] | None = None) -> RetrievalResult:
        if not query or not query.strip():
            raise RetrievalError("query cannot be empty")
        if limit < 1 or max_chars < 1:
            raise RetrievalError("limit and max_chars must be >= 1")
        hits = self.searcher.search(query, limit=limit, filters=filters)
        chunks = []
        used = 0
        for hit in hits:
            doc = hit.document
            header = f"[{doc.id}] {doc.title}".strip()
            block = f"{header}\n{doc.content}".strip()
            remaining = max_chars - used
            if remaining <= 0:
                break
            if len(block) > remaining:
                block = block[:remaining]
            chunks.append(block)
            used += len(block) + 2
            if used >= max_chars:
                break
        return RetrievalResult(
            query=query, hits=tuple(hits), context="\n\n".join(chunks),
            document_ids=tuple(hit.document.id for hit in hits),
            metadata={"index_generation": self.index.generation,
                      "returned": len(hits), "context_characters": len("\n\n".join(chunks))},
        )
