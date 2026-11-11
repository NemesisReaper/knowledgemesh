"""Identity and key revocation registry."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import threading
from typing import Iterable


class RevocationError(ValueError):
    pass


class RevocationStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class RevocationRecord:
    subject_id: str
    reason: str
    revoked_at: datetime
    revoked_by: str
    key_fingerprint: str | None = None

    def __post_init__(self):
        if not self.subject_id or not self.reason or not self.revoked_by:
            raise RevocationError("subject_id, reason and revoked_by are required")
        if self.revoked_at.tzinfo is None:
            raise RevocationError("revoked_at must be timezone-aware")


class RevocationRegistry:
    """Thread-safe in-memory registry; persist and replicate it in deployment."""
    def __init__(self, records: Iterable[RevocationRecord] = ()) -> None:
        self._records: dict[tuple[str, str | None], RevocationRecord] = {}
        self._lock = threading.RLock()
        for record in records:
            self.revoke(record)

    def revoke(self, record: RevocationRecord) -> None:
        key = (record.subject_id, record.key_fingerprint)
        with self._lock:
            existing = self._records.get(key)
            if existing and existing != record:
                raise RevocationError("subject/key is already revoked")
            self._records[key] = record

    def revoke_subject(self, subject_id: str, reason: str, revoked_by: str,
                       *, key_fingerprint: str | None = None,
                       revoked_at: datetime | None = None) -> RevocationRecord:
        record = RevocationRecord(subject_id, reason,
                                  revoked_at or datetime.now(timezone.utc),
                                  revoked_by, key_fingerprint)
        self.revoke(record)
        return record

    def status(self, subject_id: str, *, key_fingerprint: str | None = None) -> RevocationStatus:
        with self._lock:
            if (subject_id, key_fingerprint) in self._records or (subject_id, None) in self._records:
                return RevocationStatus.REVOKED
            return RevocationStatus.ACTIVE

    def is_revoked(self, subject_id: str, *, key_fingerprint: str | None = None) -> bool:
        return self.status(subject_id, key_fingerprint=key_fingerprint) == RevocationStatus.REVOKED

    def get(self, subject_id: str, *, key_fingerprint: str | None = None) -> RevocationRecord | None:
        with self._lock:
            return self._records.get((subject_id, key_fingerprint)) or self._records.get((subject_id, None))

    def records(self) -> tuple[RevocationRecord, ...]:
        with self._lock:
            return tuple(self._records.values())
