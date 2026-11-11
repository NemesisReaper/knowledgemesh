"""Artifact verification: integrity, signature validity and identity binding."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
from typing import Any, Mapping

from .identity import Identity
from .signatures import SignatureEnvelope, verify_bytes, verify_object


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    INVALID = "invalid"
    UNKNOWN_IDENTITY = "unknown_identity"
    REVOKED = "revoked"
    MISSING_SIGNATURE = "missing_signature"


@dataclass(frozen=True, slots=True)
class VerificationResult:
    status: VerificationStatus
    integrity_valid: bool
    signature_valid: bool
    signer_id: str | None
    payload_digest: str
    reasons: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def verified(self) -> bool:
        return self.status == VerificationStatus.VERIFIED


def verify_signature_envelope(payload: bytes, envelope: SignatureEnvelope | None,
                               identities: Mapping[str, Identity], *,
                               revoked_ids: set[str] | None = None,
                               expected_context: str | None = None) -> VerificationResult:
    digest = hashlib.sha256(payload).hexdigest()
    if envelope is None:
        return VerificationResult(VerificationStatus.MISSING_SIGNATURE, True, False,
                                  None, digest, ("signature envelope is missing",))
    identity = identities.get(envelope.signer_id)
    if identity is None:
        return VerificationResult(VerificationStatus.UNKNOWN_IDENTITY, True, False,
                                  envelope.signer_id, digest,
                                  ("signer identity is not trusted/known",))
    if revoked_ids and envelope.signer_id in revoked_ids:
        return VerificationResult(VerificationStatus.REVOKED, True, False,
                                  envelope.signer_id, digest,
                                  ("signer identity is revoked",))
    valid = verify_bytes(payload, envelope, identity, expected_context=expected_context)
    reasons = () if valid else ("signature, payload digest, signer binding or context invalid",)
    return VerificationResult(
        VerificationStatus.VERIFIED if valid else VerificationStatus.INVALID,
        hashlib.sha256(payload).hexdigest() == envelope.payload_digest,
        valid, envelope.signer_id, digest, reasons,
        {"algorithm": envelope.algorithm, "context": envelope.context,
         "key_fingerprint": envelope.key_fingerprint},
    )


def verify_artifact(value: Any, envelope: SignatureEnvelope | None,
                    identities: Mapping[str, Identity], *,
                    revoked_ids: set[str] | None = None,
                    expected_context: str | None = None) -> VerificationResult:
    from .signatures import canonical_json_bytes
    payload = canonical_json_bytes(value)
    return verify_signature_envelope(payload, envelope, identities,
                                      revoked_ids=revoked_ids,
                                      expected_context=expected_context)
