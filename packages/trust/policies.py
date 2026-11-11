"""Trust policy evaluation kept separate from cryptographic verification."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class PolicyError(ValueError):
    pass


class TrustLevel(str, Enum):
    UNTRUSTED = "untrusted"
    LIMITED = "limited"
    STANDARD = "standard"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class TrustPolicy:
    minimum_trust_level: TrustLevel = TrustLevel.STANDARD
    allowed_algorithms: frozenset[str] = frozenset({"Ed25519"})
    require_signature: bool = True
    require_provenance: bool = True
    reject_revoked: bool = True
    trusted_publishers: frozenset[str] = frozenset()
    required_claim_evidence: bool = False
    metadata_requirements: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reasons: tuple[str, ...]
    trust_level: TrustLevel


_TRUST_ORDER = {
    TrustLevel.UNTRUSTED: 0, TrustLevel.LIMITED: 1,
    TrustLevel.STANDARD: 2, TrustLevel.HIGH: 3,
}


def evaluate_trust(policy: TrustPolicy, *,
                   publisher_id: str | None,
                   trust_level: TrustLevel,
                   signature_present: bool,
                   signature_valid: bool,
                   algorithm: str | None = None,
                   provenance_valid: bool | None = None,
                   revoked: bool = False,
                   metadata: Mapping[str, Any] | None = None,
                   claim_has_evidence: bool | None = None) -> PolicyDecision:
    reasons = []
    if _TRUST_ORDER[trust_level] < _TRUST_ORDER[policy.minimum_trust_level]:
        reasons.append("publisher trust level is below policy minimum")
    if policy.require_signature and not signature_present:
        reasons.append("signature is required")
    if signature_present and not signature_valid:
        reasons.append("signature is invalid")
    if algorithm and algorithm not in policy.allowed_algorithms:
        reasons.append("signature algorithm is not allowed")
    if policy.require_provenance and provenance_valid is not True:
        reasons.append("valid provenance is required")
    if policy.reject_revoked and revoked:
        reasons.append("publisher or signing key is revoked")
    if policy.trusted_publishers and publisher_id not in policy.trusted_publishers:
        reasons.append("publisher is not in the trusted publisher allowlist")
    for key, expected in policy.metadata_requirements.items():
        if (metadata or {}).get(key) != expected:
            reasons.append(f"metadata requirement not met: {key}")
    if policy.required_claim_evidence and claim_has_evidence is not True:
        reasons.append("claim evidence is required")
    return PolicyDecision(not reasons, tuple(reasons), trust_level)
