"""Deterministic, dependency-free document indexing for KnowMesh."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
import re
import threading
from typing import Any, Iterable, Mapping, Sequence


class IndexingError(ValueError):
    """Raised when a document cannot be indexed safely."""


_TOKEN_RE = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Tokenize text into normalized Unicode word tokens."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return [m.group(0).casefold().replace("’", "'") for m in _TOKEN_RE.finditer(text)]


def _json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    """A searchable knowledge document.

    `id` should be stable across versions. `content_hash` is computed from
    normalized content when omitted; it is not a publisher signature.
    """
    id: str
    content: str
    title: str = ""
    bundle_id: str | None = None
    publisher_id: str | None = None
    version: str | None = None
    uri: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise IndexingError("document id cannot be empty")
        if not isinstance(self.content, str):
            raise IndexingError("document content must be a string")
        if not isinstance(self.title, str):
            raise IndexingError("document title must be a string")
        if not isinstance(self.metadata, Mapping):
            raise IndexingError("metadata must be a mapping")
        if self.updated_at.tzinfo is None:
            raise IndexingError("updated_at must be timezone-aware")
        if not self.content_hash:
            digest = _json_digest({"title": self.title, "content": self.content})
            object.__setattr__(self, "content_hash", digest)

    @property
    def searchable_text(self) -> str:
        return "\n".join(part for part in (self.title, self.content) if part)


def normalize_document(value: DocumentRecord | Mapping[str, Any]) -> DocumentRecord:
    """Convert a mapping into a validated immutable DocumentRecord."""
    if isinstance(value, DocumentRecord):
        return value
    if not isinstance(value, Mapping):
        raise IndexingError("document must be DocumentRecord or mapping")
    allowed = {
        "id", "content", "title", "bundle_id", "publisher_id", "version",
        "uri", "metadata", "updated_at", "content_hash",
    }
    unknown = set(value) - allowed
    if unknown:
        raise IndexingError(f"unknown document fields: {', '.join(sorted(unknown))}")
    data = dict(value)
    if "updated_at" in data and isinstance(data["updated_at"], str):
        try:
            data["updated_at"] = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise IndexingError("updated_at must be an ISO-8601 datetime") from exc
    return DocumentRecord(**data)


class SearchIndex:
    """Thread-safe in-memory inverted index.

    This is a local search index, not a federation registry or durable store.
    Persist source documents separately and rebuild this index when needed.
    """
    def __init__(self) -> None:
        self._documents: dict[str, DocumentRecord] = {}
        self._terms: dict[str, dict[str, int]] = {}
        self._lengths: dict[str, int] = {}
        self._lock = threading.RLock()
        self._generation = 0

    @property
    def generation(self) -> int:
        with self._lock:
            return self._generation

    def __len__(self) -> int:
        with self._lock:
            return len(self._documents)

    def get(self, document_id: str) -> DocumentRecord | None:
        with self._lock:
            return self._documents.get(document_id)

    def documents(self) -> tuple[DocumentRecord, ...]:
        with self._lock:
            return tuple(self._documents.values())

    def upsert(self, document: DocumentRecord | Mapping[str, Any]) -> DocumentRecord:
        record = normalize_document(document)
        tokens = tokenize(record.searchable_text)
        frequencies: dict[str, int] = {}
        for token in tokens:
            frequencies[token] = frequencies.get(token, 0) + 1
        with self._lock:
            self._remove_unlocked(record.id)
            self._documents[record.id] = record
            self._lengths[record.id] = len(tokens)
            for term, frequency in frequencies.items():
                self._terms.setdefault(term, {})[record.id] = frequency
            self._generation += 1
        return record

    def upsert_many(self, documents: Iterable[DocumentRecord | Mapping[str, Any]]) -> int:
        records = [normalize_document(item) for item in documents]
        ids = [item.id for item in records]
        if len(ids) != len(set(ids)):
            raise IndexingError("duplicate document ids in batch")
        for record in records:
            self.upsert(record)
        return len(records)

    def remove(self, document_id: str) -> bool:
        with self._lock:
            existed = document_id in self._documents
            if existed:
                self._remove_unlocked(document_id)
                self._generation += 1
            return existed

    def _remove_unlocked(self, document_id: str) -> None:
        self._documents.pop(document_id, None)
        self._lengths.pop(document_id, None)
        empty = []
        for term, postings in self._terms.items():
            postings.pop(document_id, None)
            if not postings:
                empty.append(term)
        for term in empty:
            self._terms.pop(term, None)

    def snapshot(self) -> tuple[tuple[DocumentRecord, ...], dict[str, dict[str, int]], dict[str, int], int]:
        with self._lock:
            return (tuple(self._documents.values()),
                    {term: dict(postings) for term, postings in self._terms.items()},
                    dict(self._lengths), self._generation)


def build_index(documents: Iterable[DocumentRecord | Mapping[str, Any]]) -> SearchIndex:
    index = SearchIndex()
    index.upsert_many(documents)
    return index
