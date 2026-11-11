import pytest
from sdk import (
    KnowMeshClient,
    SDKNotFoundError,
    SDKValidationError,
    SDKVerificationError,
    compute_payload_digest,
    create_subscription,
    delete_subscription,
    get_bundle,
    list_bundles,
    publish_bundle,
    search_knowledge,
    verify_bundle_payload,
)


def make_mock_client():
    db: dict[str, dict[str, dict]] = {}

    def transport(method: str, url: str, body, headers):
        path = url.split("http://node-a:8000/api/v1")[-1].split("?")[0]
        parts = [p for p in path.strip("/").split("/") if p]
        if url.endswith("/health"):
            return 200, {"status": "ok"}
        resource = parts[0]
        table = db.setdefault(resource, {})
        if method == "POST" and resource == "search":
            q = body["query"].casefold()
            hits = [v for t in db.values() for v in t.values() if q in str(v).casefold()]
            return 200, {"query": body["query"], "results": hits, "total": len(hits)}
        if method == "POST":
            item_id = body.get("id") or f"{resource}-1"
            record = {**body, "id": item_id}
            table[item_id] = record
            return 201, record
        if method == "GET" and len(parts) == 1:
            return 200, {"items": list(table.values())}
        if method == "GET" and len(parts) == 2:
            item = table.get(parts[1])
            if item is None:
                return 404, {"detail": "not found"}
            return 200, item
        if method == "DELETE" and len(parts) == 2:
            if parts[1] not in table:
                return 404, {"detail": "not found"}
            del table[parts[1]]
            return 204, None
        return 400, {"detail": "bad request"}

    return KnowMeshClient("http://node-a:8000", transport=transport)


def test_sdk_publish_retrieve_search_subscribe():
    client = make_mock_client()
    assert client.health()["status"] == "ok"

    created = publish_bundle(
        client,
        bundle_id="bun-1",
        title="Agent Verification Protocol",
        content="Cryptographic Ed25519 attestations",
    )
    assert created["id"] == "bun-1"
    fetched = get_bundle(client, "bun-1")
    assert fetched["title"] == "Agent Verification Protocol"
    assert len(list_bundles(client)["items"]) == 1

    hits = search_knowledge(client, "ed25519")
    assert hits["total"] == 1

    sub = create_subscription(client, subscription_id="sub-1", topic="ai-safety", subscriber_id="node-b")
    assert sub["id"] == "sub-1"
    delete_subscription(client, "sub-1")

    with pytest.raises(SDKNotFoundError):
        get_bundle(client, "nonexistent")

    with pytest.raises(SDKValidationError):
        publish_bundle(client, title="")


def test_sdk_digest_verification():
    payload = {"claim": "Water boils at 100C", "domain": "physics"}
    digest = compute_payload_digest(payload)
    bundle = {"id": "b1", "payload": payload, "digest": digest}
    assert verify_bundle_payload(bundle)
    assert not verify_bundle_payload({"id": "b1", "payload": payload, "digest": "sha256:bad"})
    with pytest.raises(SDKVerificationError):
        verify_bundle_payload({"id": "b1", "payload": payload, "digest": "sha256:bad"}, raise_on_failure=True)

