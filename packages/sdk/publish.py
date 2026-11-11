"""SDK helpers for publishing knowledge bundles, claims, and evidence."""

from __future__ import annotations

from typing import Any, Mapping

from .client import KnowMeshClient
from .exceptions import SDKValidationError


def publish_bundle(
    client: KnowMeshClient,
    *,
    title: str,
    description: str = "",
    content: str = "",
    bundle_id: str | None = None,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not title or not title.strip():
        raise SDKValidationError("bundle title is required")
    body: dict[str, Any] = {
        "title": title,
        "description": description,
        "content": content,
        "payload": dict(payload or {}),
        "metadata": dict(metadata or {}),
    }
    if bundle_id:
        body["id"] = bundle_id
    return client.request("POST", "/bundles", json_body=body)


def publish_claim(
    client: KnowMeshClient,
    *,
    title: str,
    content: str = "",
    claim_id: str | None = None,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not title or not title.strip():
        raise SDKValidationError("claim title is required")
    body: dict[str, Any] = {
        "title": title,
        "content": content,
        "payload": dict(payload or {}),
        "metadata": dict(metadata or {}),
    }
    if claim_id:
        body["id"] = claim_id
    return client.request("POST", "/claims", json_body=body)


def publish_evidence(
    client: KnowMeshClient,
    *,
    title: str,
    content: str = "",
    evidence_id: str | None = None,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not title or not title.strip():
        raise SDKValidationError("evidence title is required")
    body: dict[str, Any] = {
        "title": title,
        "content": content,
        "payload": dict(payload or {}),
        "metadata": dict(metadata or {}),
    }
    if evidence_id:
        body["id"] = evidence_id
    return client.request("POST", "/evidence", json_body=body)

