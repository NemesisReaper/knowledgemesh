"""Canonical object serialization and Ed25519 detached signatures."""

from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
import json
from typing import Any, Mapping

from .identity import Identity, KeyPair, _crypto, _b64, _unb64


class SignatureError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    """Stable project-local JSON encoding.

    This is not a claim of RFC 8785/JCS conformance. For cross-language
    signing, adopt a formally specified canonicalization profile.
    """
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SignatureError(f"object is not canonical-JSON serializable: {exc}") from exc


@dataclass(frozen=True, slots=True)
class SignatureEnvelope:
    signer_id: str
    algorithm: str
    signature: str
    payload_digest: str
    signed_at: str
    key_fingerprint: str
    context: str = "knowmesh-artifact"

    def __post_init__(self):
        if self.algorithm != "Ed25519":
            raise SignatureError("unsupported signature algorithm")
        if not self.signer_id or not self.signature or not self.payload_digest:
            raise SignatureError("incomplete signature envelope")
        if len(_unb64(self.signature)) != 64:
            raise SignatureError("Ed25519 signature must be 64 bytes")

    def to_dict(self) -> dict[str, str]:
        return {
            "signer_id": self.signer_id, "algorithm": self.algorithm,
            "signature": self.signature, "payload_digest": self.payload_digest,
            "signed_at": self.signed_at, "key_fingerprint": self.key_fingerprint,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "SignatureEnvelope":
        return cls(**dict(value))


def sign_bytes(payload: bytes, keypair: KeyPair, *, context: str = "knowmesh-artifact",
               signed_at: str | None = None) -> SignatureEnvelope:
    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")
    if not context:
        raise SignatureError("signature context is required")
    Ed25519PrivateKey, _, _ = _crypto()
    try:
        private = Ed25519PrivateKey.from_private_bytes(keypair.private_key_bytes)
        signature = private.sign(payload)
    except Exception as exc:
        raise SignatureError("unable to sign payload") from exc
    from datetime import datetime, timezone
    timestamp = signed_at or datetime.now(timezone.utc).isoformat()
    return SignatureEnvelope(
        signer_id=keypair.identity.id, algorithm="Ed25519",
        signature=_b64(signature),
        payload_digest=hashlib.sha256(payload).hexdigest(),
        signed_at=timestamp,
        key_fingerprint=keypair.identity.fingerprint,
        context=context,
    )


def sign_object(value: Any, keypair: KeyPair, *, context: str = "knowmesh-artifact",
                signed_at: str | None = None) -> SignatureEnvelope:
    return sign_bytes(canonical_json_bytes(value), keypair,
                      context=context, signed_at=signed_at)


def verify_bytes(payload: bytes, envelope: SignatureEnvelope,
                 identity: Identity, *, expected_context: str | None = None) -> bool:
    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")
    if envelope.signer_id != identity.id:
        return False
    if envelope.key_fingerprint != identity.fingerprint:
        return False
    if expected_context is not None and envelope.context != expected_context:
        return False
    if hashlib.sha256(payload).hexdigest() != envelope.payload_digest:
        return False
    _, Ed25519PublicKey, _ = _crypto()
    try:
        Ed25519PublicKey.from_public_bytes(identity.public_key_bytes).verify(
            _unb64(envelope.signature), payload
        )
        return True
    except Exception:
        return False


def verify_object(value: Any, envelope: SignatureEnvelope, identity: Identity,
                  *, expected_context: str | None = None) -> bool:
    try:
        payload = canonical_json_bytes(value)
    except SignatureError:
        return False
    return verify_bytes(payload, envelope, identity, expected_context=expected_context)
