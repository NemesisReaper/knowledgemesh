"""SDK helpers for managing topic and bundle subscriptions."""

from __future__ import annotations

from typing import Any, Mapping

from .client import KnowMeshClient
from .exceptions import SDKValidationError


def create_subscription(
    client: KnowMeshClient,
    *,
    topic: str,
    subscriber_id: str,
    subscription_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not topic or not topic.strip():
        raise SDKValidationError("subscription topic is required")
    if not subscriber_id or not subscriber_id.strip():
        raise SDKValidationError("subscriber_id is required")
    body: dict[str, Any] = {
        "name": topic,
        "payload": {"topic": topic, "subscriber_id": subscriber_id},
        "metadata": dict(metadata or {}),
    }
    if subscription_id:
        body["id"] = subscription_id
    return client.request("POST", "/subscriptions", json_body=body)


def list_subscriptions(client: KnowMeshClient, *, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return client.request("GET", "/subscriptions", params={"limit": limit, "offset": offset})


def delete_subscription(client: KnowMeshClient, subscription_id: str) -> None:
    if not subscription_id or not subscription_id.strip():
        raise SDKValidationError("subscription_id is required")
    client.request("DELETE", f"/subscriptions/{subscription_id}")

