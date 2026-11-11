from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json
from typing import Any, Mapping

def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")

def identity_fingerprint(payload: Mapping[str, Any]) -> str:
    """Stable SHA-256 fingerprint of a JSON-compatible knowledge payload."""
    return hashlib.sha256(_canonical(payload)).hexdigest()

@dataclass(frozen=True)
class KnowledgeIdentity:
    """Stable logical identity, distinct from a content/version fingerprint."""
    knowledge_id: str
    namespace: str = "default"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "1"

    def __post_init__(self):
        if not self.knowledge_id.strip() or not self.namespace.strip():
            raise ValueError("knowledge_id and namespace must be non-empty")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

    @property
    def qualified_id(self) -> str:
        return f"{self.namespace}:{self.knowledge_id}"

    def to_dict(self) -> dict[str, str]:
        return {"knowledge_id": self.knowledge_id, "namespace": self.namespace,
                "created_at": self.created_at.astimezone(timezone.utc).isoformat(),
                "schema_version": self.schema_version}
