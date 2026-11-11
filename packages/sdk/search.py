"""SDK helper for searching across a KnowMesh node."""

from __future__ import annotations

from typing import Any

from .client import KnowMeshClient
from .exceptions import SDKValidationError


def search_knowledge(
    client: KnowMeshClient,
    query: str,
    *,
    limit: int = 10,
    scope: str | None = None,
) -> dict[str, Any]:
    if not query or not query.strip():
        raise SDKValidationError("search query cannot be empty")
    if limit < 1 or limit > 100:
        raise SDKValidationError("limit must be between 1 and 100")
    body: dict[str, Any] = {"query": query, "limit": limit}
    if scope:
        body["scope"] = scope
    return client.request("POST", "/search", json_body=body)
