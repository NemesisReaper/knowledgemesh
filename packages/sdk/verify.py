"""Client-side digest and Ed25519 cryptographic verification helpers for the KnowMesh SDK."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from okf import calculate_canonical_hash
from trust import Identity as TrustIdentity, SignatureEnvelope, verify_artifact

from .exceptions import SDKVerificationError


def compute_payload_digest(payload: Mapping[str, Any]) -> str:
    canonical = json.dumps(dict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def verify_bundle_payload(
    bundle: Mapping[str, Any],
    *,
    expected_digest: str | None = None,
    raise_on_failure: bool = False,
) -> bool:
    """Verify a bundle's canonical payload digest."""
    payload = bundle.get("payload") if isinstance(bundle.get("payload"), Mapping) else bundle
    target_digest = expected_digest or str(bundle.get("digest") or bundle.get("content_digest") or "")
    if not target_digest:
        if raise_on_failure:
            raise SDKVerificationError("No expected digest present on bundle")
        return False
    if not target_digest.startswith("sha256:"):
        target_digest = f"sha256:{target_digest}"
    computed = compute_payload_digest(payload)
    valid = computed.lower() == target_digest.lower()
    if not valid and raise_on_failure:
        raise SDKVerificationError(f"Bundle digest mismatch: expected {target_digest}, got {computed}")
    return valid


def verify_bundle_signature(
    bundle: Mapping[str, Any],
    *,
    public_key: str,
    raise_on_failure: bool = False,
) -> dict[str, Any]:
    """Cryptographically verify a retrieved KnowMesh bundle's OKF digest and Ed25519 signature client-side."""
    manifest_raw = dict(bundle.get("okf_manifest") or bundle)
    canonical_payload = {
        k: manifest_raw[k]
        for k in (
            "bundle_id",
            "title",
            "version",
            "format_version",
            "publisher_id",
            "description",
            "claims",
            "evidence",
            "links",
            "metadata",
        )
        if k in manifest_raw
    }
    computed_digest = calculate_canonical_hash(canonical_payload)
    reported_digest = str(bundle.get("content_digest") or manifest_raw.get("digest") or "")
    integrity_valid = bool(reported_digest) and computed_digest.lower() == reported_digest.lower()

    sig_raw = bundle.get("signature")
    if not isinstance(sig_raw, Mapping):
        if raise_on_failure:
            raise SDKVerificationError("Bundle is missing signature envelope")
        return {"verified": False, "integrity_verified": integrity_valid, "signature_verified": False}

    envelope = SignatureEnvelope.from_dict(sig_raw)
    ident = TrustIdentity(id=envelope.signer_id, public_key=public_key)
    res = verify_artifact(
        canonical_payload,
        envelope,
        {envelope.signer_id: ident},
        expected_context="knowmesh-okf-bundle",
    )
    verified = integrity_valid and res.verified
    if not verified and raise_on_failure:
        raise SDKVerificationError(
            f"Bundle cryptographic verification failed: integrity={integrity_valid}, reasons={res.reasons}"
        )
    return {
        "verified": verified,
        "integrity_verified": integrity_valid,
        "signature_verified": res.signature_valid and integrity_valid,
        "signer_id": envelope.signer_id,
        "key_fingerprint": envelope.key_fingerprint,
        "computed_digest": computed_digest,
        "reported_digest": reported_digest,
        "reasons": list(res.reasons),
    }
