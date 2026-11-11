"""Open Knowledge Format (OKF) manifest and artifact models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .hashing import calculate_canonical_hash, compute_merkle_root
from .issues import OKFError
from .links import OKFLink

SUPPORTED_FORMAT_VERSIONS = frozenset({"0.1", "0.2", "1.0"})


@dataclass(frozen=True, slots=True)
class OKFClaim:
    claim_id: str
    statement: str
    domain: str = "general"
    status: str = "proposed"
    evidence_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.claim_id or not self.claim_id.strip():
            raise OKFError("claim_id is required")
        if not self.statement or not self.statement.strip():
            raise OKFError("claim statement is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "statement": self.statement,
            "domain": self.domain,
            "status": self.status,
            "evidence_ids": list(self.evidence_ids),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OKFClaim":
        return cls(
            claim_id=str(data.get("claim_id") or data.get("id") or ""),
            statement=str(data.get("statement") or data.get("text") or ""),
            domain=str(data.get("domain") or "general"),
            status=str(data.get("status") or "proposed"),
            evidence_ids=tuple(str(x) for x in (data.get("evidence_ids") or ())),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(frozen=True, slots=True)
class OKFEvidence:
    evidence_id: str
    source_uri: str = ""
    source_type: str = "reference"
    description: str = ""
    content_hash: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.evidence_id.strip():
            raise OKFError("evidence_id is required")
        if not self.content_hash:
            digest = calculate_canonical_hash(
                {
                    "evidence_id": self.evidence_id,
                    "source_uri": self.source_uri,
                    "source_type": self.source_type,
                    "description": self.description,
                }
            )
            object.__setattr__(self, "content_hash", digest)

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source_uri": self.source_uri,
            "source_type": self.source_type,
            "description": self.description,
            "content_hash": self.content_hash,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OKFEvidence":
        return cls(
            evidence_id=str(data.get("evidence_id") or data.get("id") or ""),
            source_uri=str(data.get("source_uri") or data.get("uri") or ""),
            source_type=str(data.get("source_type") or data.get("evidence_type") or "reference"),
            description=str(data.get("description") or ""),
            content_hash=str(data.get("content_hash") or ""),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(frozen=True, slots=True)
class OKFManifest:
    bundle_id: str
    title: str
    version: str = "1.0.0"
    format_version: str = "0.2"
    publisher_id: str = "unknown"
    description: str = ""
    claims: tuple[OKFClaim, ...] = ()
    evidence: tuple[OKFEvidence, ...] = ()
    links: tuple[OKFLink, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    digest: str = ""
    merkle_root: str = ""

    def __post_init__(self) -> None:
        if not self.bundle_id or not self.bundle_id.strip():
            raise OKFError("bundle_id is required")
        if not self.title or not self.title.strip():
            raise OKFError("manifest title is required")
        if not self.version or not str(self.version).strip():
            raise OKFError("manifest version is required")
        computed_digest = self.compute_digest()
        if not self.digest:
            object.__setattr__(self, "digest", computed_digest)
        computed_merkle = self.compute_merkle_root()
        if not self.merkle_root:
            object.__setattr__(self, "merkle_root", computed_merkle)

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "title": self.title,
            "version": str(self.version),
            "format_version": self.format_version,
            "publisher_id": self.publisher_id,
            "description": self.description,
            "claims": [c.to_dict() for c in self.claims],
            "evidence": [e.to_dict() for e in self.evidence],
            "links": [l.to_dict() for l in self.links],
            "metadata": dict(self.metadata),
        }

    def compute_digest(self) -> str:
        return calculate_canonical_hash(self.canonical_payload())

    def compute_merkle_root(self) -> str:
        leaf_hashes = [calculate_canonical_hash(c.to_dict()) for c in self.claims] + [
            e.content_hash for e in self.evidence
        ]
        return compute_merkle_root(leaf_hashes)

    def to_dict(self) -> dict[str, Any]:
        payload = self.canonical_payload()
        payload["digest"] = self.digest
        payload["merkle_root"] = self.merkle_root
        return payload

