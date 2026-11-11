"""Artifact and URI resolver for Open Knowledge Format (OKF) bundles."""

from __future__ import annotations

from typing import Any

from .issues import OKFError
from .links import parse_okf_uri
from .manifest import OKFClaim, OKFEvidence, OKFManifest


class OKFResolver:
    """In-memory registry for resolving OKF bundles, claims, and evidence by URI or ID."""

    def __init__(self, manifests: tuple[OKFManifest, ...] | list[OKFManifest] = ()) -> None:
        self._manifests: dict[str, OKFManifest] = {}
        for manifest in manifests:
            self.register(manifest)

    def register(self, manifest: OKFManifest) -> None:
        self._manifests[manifest.bundle_id] = manifest

    def get_bundle(self, bundle_id: str) -> OKFManifest | None:
        return self._manifests.get(bundle_id)

    def resolve(self, uri: str) -> OKFManifest | OKFClaim | OKFEvidence:
        """Resolve 'okf://<bundle_id>' or 'okf://<bundle_id>/<artifact_id>'."""
        bundle_id, item_id = parse_okf_uri(uri)
        manifest = self._manifests.get(bundle_id)
        if manifest is None:
            raise OKFError(f"bundle not found: {bundle_id}")
        if item_id is None:
            return manifest
        for claim in manifest.claims:
            if claim.claim_id == item_id:
                return claim
        for ev in manifest.evidence:
            if ev.evidence_id == item_id:
                return ev
        raise OKFError(f"artifact {item_id!r} not found in bundle {bundle_id!r}")

    def resolve_claim_evidence(self, bundle_id: str, claim_id: str) -> tuple[OKFEvidence, ...]:
        manifest = self._manifests.get(bundle_id)
        if manifest is None:
            raise OKFError(f"bundle not found: {bundle_id}")
        claim = next((c for c in manifest.claims if c.claim_id == claim_id), None)
        if claim is None:
            raise OKFError(f"claim not found: {claim_id}")
        by_id = {e.evidence_id: e for e in manifest.evidence}
        missing = [eid for eid in claim.evidence_ids if eid not in by_id]
        if missing:
            raise OKFError(f"missing evidence references for claim {claim_id}: {missing}")
        return tuple(by_id[eid] for eid in claim.evidence_ids)

