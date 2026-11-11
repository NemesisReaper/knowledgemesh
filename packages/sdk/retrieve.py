"""SDK helpers for retrieving knowledge bundles, claims, and evidence."""

from __future__ import annotations

from typing import Any

from .client import KnowMeshClient
from .exceptions import SDKValidationError


def get_bundle(client: KnowMeshClient, bundle_id: str) -> dict[str, Any]:
    if not bundle_id or not bundle_id.strip():
        raise SDKValidationError("bundle_id is required")
    return client.request("GET", f"/bundles/{bundle_id}")


def list_bundles(client: KnowMeshClient, *, limit: int = 50, offset: int = 0, q: str | None = None) -> dict[str, Any]:
    return client.request("GET", "/bundles", params={"limit": limit, "offset": offset, "q": q})


def get_claim(client: KnowMeshClient, claim_id: str) -> dict[str, Any]:
    if not claim_id or not claim_id.strip():
        raise SDKValidationError("claim_id is required")
    return client.request("GET", f"/claims/{claim_id}")


def get_evidence(client: KnowMeshClient, evidence_id: str) -> dict[str, Any]:
    if not evidence_id or not evidence_id.strip():
        raise SDKValidationError("evidence_id is required")
    return client.request("GET", f"/evidence/{evidence_id}")

