"""KnowMesh Python SDK for publishing, retrieving, searching, subscribing, and verifying knowledge."""

from .client import KnowMeshClient
from .exceptions import (
    SDKConnectionError,
    SDKError,
    SDKNotFoundError,
    SDKValidationError,
    SDKVerificationError,
)
from .publish import publish_bundle, publish_claim, publish_evidence
from .retrieve import get_bundle, get_claim, get_evidence, list_bundles
from .search import search_knowledge
from .subscribe import create_subscription, delete_subscription, list_subscriptions
from .verify import compute_payload_digest, verify_bundle_payload, verify_bundle_signature

__all__ = [
    "KnowMeshClient",
    "SDKError",
    "SDKConnectionError",
    "SDKNotFoundError",
    "SDKValidationError",
    "SDKVerificationError",
    "publish_bundle",
    "publish_claim",
    "publish_evidence",
    "get_bundle",
    "list_bundles",
    "get_claim",
    "get_evidence",
    "search_knowledge",
    "create_subscription",
    "list_subscriptions",
    "delete_subscription",
    "compute_payload_digest",
    "verify_bundle_payload",
    "verify_bundle_signature",
]
