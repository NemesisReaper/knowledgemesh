"""Parser for Open Knowledge Format (OKF) manifests and bundle payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .issues import OKFError
from .links import OKFLink
from .manifest import OKFClaim, OKFEvidence, OKFManifest


def parse_manifest(source: str | bytes | Path | Mapping[str, Any]) -> OKFManifest:
    """Parse an OKFManifest from a dictionary, JSON string/bytes, or file path."""
    if isinstance(source, Path):
        try:
            raw = json.loads(source.read_text(encoding="utf-8"))
        except Exception as exc:
            raise OKFError(f"failed to read OKF file {source}: {exc}") from exc
    elif isinstance(source, (str, bytes)):
        try:
            raw = json.loads(source)
        except Exception as exc:
            raise OKFError(f"invalid OKF JSON: {exc}") from exc
    elif isinstance(source, Mapping):
        raw = dict(source)
    else:
        raise OKFError(f"unsupported OKF source type: {type(source).__name__}")

    if not isinstance(raw, Mapping):
        raise OKFError("OKF manifest root must be a JSON object")

    claims = tuple(OKFClaim.from_dict(item) for item in (raw.get("claims") or ()))
    evidence = tuple(OKFEvidence.from_dict(item) for item in (raw.get("evidence") or ()))
    links = tuple(OKFLink.from_dict(item) for item in (raw.get("links") or ()))

    return OKFManifest(
        bundle_id=str(raw.get("bundle_id") or raw.get("id") or ""),
        title=str(raw.get("title") or ""),
        version=str(raw.get("version") or "1.0.0"),
        format_version=str(raw.get("format_version") or "0.2"),
        publisher_id=str(raw.get("publisher_id") or raw.get("node_id") or "unknown"),
        description=str(raw.get("description") or ""),
        claims=claims,
        evidence=evidence,
        links=links,
        metadata=dict(raw.get("metadata") or {}),
        digest=str(raw.get("digest") or ""),
        merkle_root=str(raw.get("merkle_root") or ""),
    )

