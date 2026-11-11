"""Append-only, hash-linked provenance records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Iterable, Mapping


class ProvenanceError(ValueError):
    pass


class ProvenanceAction(str, Enum):
    CREATED = "created"
    IMPORTED = "imported"
    TRANSFORMED = "transformed"
    REVIEWED = "reviewed"
    VERIFIED = "verified"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    record_id: str
    subject_id: str
    action: ProvenanceAction
    actor_id: str
    timestamp: datetime
    details: Mapping[str, Any] = field(default_factory=dict)
    previous_hash: str | None = None
    record_hash: str = ""

    def __post_init__(self):
        if not self.record_id or not self.subject_id or not self.actor_id:
            raise ProvenanceError("record_id, subject_id and actor_id are required")
        if self.timestamp.tzinfo is None:
            raise ProvenanceError("timestamp must be timezone-aware")
        expected = self.compute_hash()
        if self.record_hash and self.record_hash != expected:
            raise ProvenanceError("provenance record hash mismatch")
        object.__setattr__(self, "record_hash", expected)

    def hash_payload(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id, "subject_id": self.subject_id,
            "action": self.action.value, "actor_id": self.actor_id,
            "timestamp": self.timestamp.isoformat(),
            "details": dict(self.details), "previous_hash": self.previous_hash,
        }

    def compute_hash(self) -> str:
        return hashlib.sha256(_canonical(self.hash_payload())).hexdigest()


class ProvenanceChain:
    """In-memory append-only chain for a single subject."""
    def __init__(self, subject_id: str, records: Iterable[ProvenanceRecord] = ()) -> None:
        if not subject_id:
            raise ProvenanceError("subject_id is required")
        self.subject_id = subject_id
        self._records: list[ProvenanceRecord] = []
        for record in records:
            self.append(record)

    def append(self, record: ProvenanceRecord) -> ProvenanceRecord:
        if record.subject_id != self.subject_id:
            raise ProvenanceError("record subject does not match chain")
        expected_previous = self._records[-1].record_hash if self._records else None
        if record.previous_hash != expected_previous:
            raise ProvenanceError("record does not extend current chain head")
        if any(existing.record_id == record.record_id for existing in self._records):
            raise ProvenanceError("duplicate provenance record id")
        self._records.append(record)
        return record

    def add(self, *, record_id: str, action: ProvenanceAction, actor_id: str,
            details: Mapping[str, Any] | None = None,
            timestamp: datetime | None = None) -> ProvenanceRecord:
        previous = self._records[-1].record_hash if self._records else None
        record = ProvenanceRecord(
            record_id, self.subject_id, action, actor_id,
            timestamp or datetime.now(timezone.utc), details or {}, previous,
        )
        return self.append(record)

    def verify(self) -> bool:
        previous = None
        seen = set()
        for record in self._records:
            if record.subject_id != self.subject_id or record.previous_hash != previous:
                return False
            if record.record_id in seen or record.compute_hash() != record.record_hash:
                return False
            previous = record.record_hash
            seen.add(record.record_id)
        return True

    @property
    def head_hash(self) -> str | None:
        return self._records[-1].record_hash if self._records else None

    def records(self) -> tuple[ProvenanceRecord, ...]:
        return tuple(self._records)
