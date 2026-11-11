from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json
from typing import Any, Mapping

def _digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()

@dataclass(frozen=True)
class HistoryEntry:
    revision: int
    knowledge_id: str
    payload: dict[str, Any]
    fingerprint: str
    previous_fingerprint: str | None
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = "unknown"
    change_note: str = ""

class KnowledgeHistory:
    """In-memory append-only revision history with a hash-linked sequence."""
    def __init__(self, knowledge_id: str):
        if not knowledge_id: raise ValueError("knowledge_id required")
        self.knowledge_id = knowledge_id
        self._entries: list[HistoryEntry] = []

    def record(self, payload: Mapping[str, Any], *, actor="unknown", change_note="") -> HistoryEntry:
        snapshot = deepcopy(dict(payload))
        previous = self._entries[-1].fingerprint if self._entries else None
        fingerprint = _digest({"knowledge_id": self.knowledge_id, "revision": len(self._entries)+1,
                               "previous": previous, "payload": snapshot})
        entry = HistoryEntry(len(self._entries)+1, self.knowledge_id, snapshot, fingerprint,
                             previous, actor=actor, change_note=change_note)
        self._entries.append(entry)
        return entry

    def get(self, revision: int) -> HistoryEntry:
        if revision < 1: raise IndexError("revision numbers start at 1")
        return self._entries[revision-1]

    @property
    def latest(self) -> HistoryEntry | None:
        return self._entries[-1] if self._entries else None

    def revisions(self) -> tuple[HistoryEntry, ...]: return tuple(self._entries)

    def verify(self) -> bool:
        previous = None
        for i, entry in enumerate(self._entries, 1):
            expected = _digest({"knowledge_id": self.knowledge_id, "revision": i,
                                "previous": previous, "payload": entry.payload})
            if entry.revision != i or entry.previous_fingerprint != previous or entry.fingerprint != expected:
                return False
            previous = entry.fingerprint
        return True
