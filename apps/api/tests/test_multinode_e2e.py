"""End-to-End 3-Node Federation Acceptance Test Suite (Directive Section 5.3 & 5.4).

Demonstrates and verifies:
1. Node A (Alpha Research) creates organization, node, agent, and publishes Knowledge Bundle v1 (1.0.0)
   with claims, evidence, sources, deterministic OKF digest, and Ed25519 signature.
2. Node B (Beta Intelligence) connects to Node A, verifies peer identity & Ed25519 key fingerprint,
   discovers Bundle v1 over federated search, retrieves v1, verifies signature + digest, and stores v1 locally.
3. Node A publishes Revision v2 (1.1.0) updating claims and evidence.
4. Node B runs pull-based synchronization with Node A, detects the revision update, verifies v2,
   compares revision diff (1.0.0 -> 1.1.0), and retains historical revision 1.0.0 alongside 1.1.0.
5. Node C (Gamma Observatory) connects to the federated network, discovers Revision v2 (1.1.0),
   retrieves it, and verifies its provenance and cryptographic signature.
6. Security & Negative Tests:
   - Private bundle on Node A is never exposed in federated discovery or federated retrieval (403 denied).
   - Tampered bundle payload from a peer is rejected by cryptographic digest & Ed25519 signature verification.
   - Offline/unreachable peer is handled gracefully during federated search with circuit-breaker/trace reporting.
"""

from __future__ import annotations

import copy
from typing import Any, Mapping
import urllib.parse
from fastapi.testclient import TestClient

from knowmesh_api.config import Settings
from knowmesh_api.main import create_app
from knowmesh_api.service import KnowMeshService


def build_three_node_network() -> dict[str, TestClient]:
    """Create 3 independent KnowMesh nodes (node-a, node-b, node-c) with isolated databases and Ed25519 keys."""
    clients: dict[str, TestClient] = {}

    def peer_router(method: str, url: str, json_body: Mapping[str, Any] | None, headers: Mapping[str, str] | None) -> tuple[int, Any]:
        parsed = urllib.parse.urlsplit(url)
        host_key = f"{parsed.scheme}://{parsed.netloc}"
        target_client = clients.get(host_key)
        if target_client is None:
            raise ConnectionError(f"Peer endpoint {host_key} is offline or unreachable")
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        resp = target_client.request(method, path, json=dict(json_body) if json_body is not None else None, headers=dict(headers or {}))
        return resp.status_code, (resp.json() if resp.content else None)

    node_configs = [
        ("node-a", "Alpha Research Node", "http://node-a.local:8001"),
        ("node-b", "Beta Intelligence Node", "http://node-b.local:8002"),
        ("node-c", "Gamma Observatory Node", "http://node-c.local:8003"),
    ]
    for nid, name, endpoint in node_configs:
        cfg = Settings(
            app_name=f"KnowMesh ({nid})",
            node_id=nid,
            node_name=name,
            node_endpoint=endpoint,
            database_url="sqlite:///:memory:",
            secret_key=f"secret-key-{nid}-0123456789abcdef",
            allow_local_peers=True,
        )
        svc = KnowMeshService(cfg, peer_http=peer_router)
        app = create_app(cfg, service=svc)
        clients[endpoint] = TestClient(app, base_url=endpoint)
        clients[nid] = clients[endpoint]

    return clients


def test_three_node_federated_lifecycle_and_security() -> None:
    net = build_three_node_network()
    node_a = net["node-a"]
    node_b = net["node-b"]
    node_c = net["node-c"]

    # ------------------------------------------------------------------
    # 1. Node A: Register user, organization, agent, and publish Bundle v1
    # ------------------------------------------------------------------
    reg_a = node_a.post(
        "/api/v1/auth/register",
        json={
            "email": "curator@alpha.org",
            "password": "AlphaPassword!2026",
            "full_name": "Dr. Ada Lovelace",
            "organization_name": "Alpha Federated Research",
        },
    )
    assert reg_a.status_code == 201
    token_a = reg_a.json()["access_token"]

    agent_a = node_a.post(
        "/api/v1/agents",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "name": "AlphaPublisherAgent",
            "permissions": [
                "knowledge:read",
                "knowledge:search",
                "knowledge:publish",
                "knowledge:update",
                "verification:read",
            ],
        },
    )
    assert agent_a.status_code == 201
    agent_a_key = agent_a.json()["initial_credential"]["secret"]

    v1_pub = node_a.post(
        "/api/v1/bundles",
        headers={"X-KnowMesh-Key": agent_a_key},
        json={
            "bundle_id": "bun-quantum-routing",
            "title": "Fault-Tolerant Quantum Repeater Routing",
            "description": "Entanglement swapping fidelity benchmarks across metropolitan fiber links",
            "category": "quantum-networking",
            "visibility": "federated",
            "version": "1.0.0",
            "claims": [
                {
                    "claim_id": "cl-qr-1",
                    "statement": "Purified entanglement links maintain 94.2% Bell-state fidelity over 45km deployed fiber.",
                    "status": "supported",
                    "evidence_ids": ["ev-qr-1"],
                }
            ],
            "evidence": [
                {
                    "evidence_id": "ev-qr-1",
                    "title": "Metro Fiber Telemetry Run #408",
                    "source_uri": "https://alpha.org/datasets/qr-408",
                    "description": "Coincidence count tomography dataset over 72 hours",
                }
            ],
        },
    )
    assert v1_pub.status_code == 201
    bundle_v1 = v1_pub.json()
    v1_digest = bundle_v1["content_digest"]
    assert bundle_v1["revision"] == "1.0.0"
    assert bundle_v1["verification"]["status"] == "verified"

    # ------------------------------------------------------------------
    # 2. Node B: Connect to Node A, verify identity, discover & retrieve v1
    # ------------------------------------------------------------------
    peer_ab = node_b.post(
        "/api/v1/federation/peers",
        json={
            "name": "Alpha Research Node",
            "endpoint": "http://node-a.local:8001",
            "auto_approve": True,
        },
    )
    assert peer_ab.status_code == 201
    peer_ab_data = peer_ab.json()
    assert peer_ab_data["peer_node_id"] == "node-a"
    assert peer_ab_data["identity_verified"] is True
    assert peer_ab_data["approved"] is True

    # Node B executes federated search across connected peers
    disc_b = node_b.post(
        "/api/v1/search",
        json={"query": "entanglement swapping", "scope": "federated"},
    )
    assert disc_b.status_code == 200
    disc_b_data = disc_b.json()
    assert disc_b_data["total"] == 1
    assert disc_b_data["results"][0]["bundle_id"] == "bun-quantum-routing"
    assert disc_b_data["results"][0]["publisher_node"] == "node-a"
    assert disc_b_data["results"][0]["verification_status"] == "verified"

    # Node B retrieves and persists Bundle v1 from Node A, verifying signature & digest
    ret_b = node_b.post(
        "/api/v1/federation/retrieve",
        json={"peer_id": "node-a", "bundle_id": "bun-quantum-routing", "persist": True},
    )
    assert ret_b.status_code == 200
    stored_on_b_v1 = ret_b.json()
    assert stored_on_b_v1["revision"] == "1.0.0"
    assert stored_on_b_v1["content_digest"] == v1_digest
    assert stored_on_b_v1["verification"]["integrity_verified"] is True
    assert stored_on_b_v1["verification"]["signature_verified"] is True
    assert stored_on_b_v1["verification"]["signer_recognized"] is True

    # ------------------------------------------------------------------
    # 3. Node A publishes Revision v2 (1.1.0)
    # ------------------------------------------------------------------
    v2_pub = node_a.post(
        "/api/v1/bundles/bun-quantum-routing/revisions",
        headers={"X-KnowMesh-Key": agent_a_key},
        json={
            "version": "1.1.0",
            "description": "Entanglement swapping fidelity benchmarks across 45km and 90km multi-hop links",
            "change_note": "Added two-hop repeater benchmark claim cl-qr-2",
            "claims": [
                {
                    "claim_id": "cl-qr-1",
                    "statement": "Purified entanglement links maintain 94.2% Bell-state fidelity over 45km deployed fiber.",
                    "status": "supported",
                    "evidence_ids": ["ev-qr-1"],
                },
                {
                    "claim_id": "cl-qr-2",
                    "statement": "Two-hop repeater chains sustain 88.7% end-to-end fidelity across 90km with active phase stabilization.",
                    "status": "supported",
                    "evidence_ids": ["ev-qr-1", "ev-qr-2"],
                },
            ],
            "evidence": [
                {
                    "evidence_id": "ev-qr-1",
                    "title": "Metro Fiber Telemetry Run #408",
                    "source_uri": "https://alpha.org/datasets/qr-408",
                    "description": "Coincidence count tomography dataset over 72 hours",
                },
                {
                    "evidence_id": "ev-qr-2",
                    "title": "Multi-Hop Phase Stabilization Log #512",
                    "source_uri": "https://alpha.org/datasets/qr-512",
                    "description": "Interferometric phase lock loop telemetry across 90km",
                },
            ],
        },
    )
    assert v2_pub.status_code == 201
    v2_digest = v2_pub.json()["content_digest"]
    assert v2_digest != v1_digest

    # ------------------------------------------------------------------
    # 4. Node B synchronizes with Node A, detects update, diffs, retains v1
    # ------------------------------------------------------------------
    sync_b = node_b.post("/api/v1/federation/peers/node-a/sync")
    assert sync_b.status_code == 200
    sync_b_data = sync_b.json()
    assert sync_b_data["state"] == "succeeded"
    assert "bun-quantum-routing" in sync_b_data["updated_bundle_ids"]

    # Node B now has revision 1.1.0 as current AND retains 1.0.0 in revision history
    latest_on_b = node_b.get("/api/v1/bundles/bun-quantum-routing").json()
    assert latest_on_b["current_revision"] == "1.1.0"
    assert latest_on_b["content_digest"] == v2_digest
    assert latest_on_b["verification"]["status"] == "verified"

    revs_on_b = [r["revision"] for r in latest_on_b["revisions"]]
    assert "1.0.0" in revs_on_b
    assert "1.1.0" in revs_on_b

    # Historical retrieval of v1 on Node B still returns exact v1 payload & digest
    hist_v1_on_b = node_b.get("/api/v1/bundles/bun-quantum-routing?revision=1.0.0").json()
    assert hist_v1_on_b["revision"] == "1.0.0"
    assert hist_v1_on_b["content_digest"] == v1_digest

    # Node B compares diff between 1.0.0 and 1.1.0
    diff_b = node_b.get("/api/v1/bundles/bun-quantum-routing/diff?from_rev=1.0.0&to_rev=1.1.0").json()
    assert diff_b["changed"] is True
    assert len(diff_b["added_claims"]) == 1
    assert diff_b["added_claims"][0]["claim_id"] == "cl-qr-2"

    # ------------------------------------------------------------------
    # 5. Node C connects to the network, discovers v2, and verifies it
    # ------------------------------------------------------------------
    peer_cb = node_c.post(
        "/api/v1/federation/peers",
        json={
            "name": "Beta Intelligence Node",
            "endpoint": "http://node-b.local:8002",
            "auto_approve": True,
        },
    )
    assert peer_cb.status_code == 201
    # Also register Node A's public identity on Node C so Node C recognizes original signer Node A
    peer_ca = node_c.post(
        "/api/v1/federation/peers",
        json={
            "name": "Alpha Research Node",
            "endpoint": "http://node-a.local:8001",
            "auto_approve": True,
        },
    )
    assert peer_ca.status_code == 201

    disc_c = node_c.post(
        "/api/v1/search",
        json={"query": "phase stabilization", "scope": "federated"},
    )
    assert disc_c.status_code == 200
    disc_c_hits = disc_c.json()["results"]
    assert len(disc_c_hits) >= 1
    assert disc_c_hits[0]["revision"] == "1.1.0"

    ret_c = node_c.post(
        "/api/v1/federation/retrieve",
        json={"peer_id": "node-b", "bundle_id": "bun-quantum-routing", "persist": True},
    )
    assert ret_c.status_code == 200
    bundle_on_c = ret_c.json()
    assert bundle_on_c["revision"] == "1.1.0"
    assert bundle_on_c["verification"]["status"] == "verified"
    assert bundle_on_c["verification"]["signer_id"] == "node-a"

    # ------------------------------------------------------------------
    # 6. Security & Negative Tests: Private Bundle Denial, Tampering, Offline Peer
    # ------------------------------------------------------------------
    # 6a. Node A publishes a PRIVATE bundle; Node B must not discover or retrieve it
    priv_pub = node_a.post(
        "/api/v1/bundles",
        headers={"X-KnowMesh-Key": agent_a_key},
        json={
            "bundle_id": "bun-alpha-secret",
            "title": "Proprietary Cryogenic ASIC Layout",
            "description": "Confidential internal circuit parameters",
            "visibility": "private",
            "claims": [{"statement": "Internal cryo-CMOS bias voltage is 0.42V."}],
        },
    )
    assert priv_pub.status_code == 201

    priv_search_b = node_b.post(
        "/api/v1/search",
        json={"query": "Cryogenic ASIC", "scope": "federated"},
    ).json()
    assert priv_search_b["total"] == 0

    priv_ret_b = node_b.post(
        "/api/v1/federation/retrieve",
        json={"peer_id": "node-a", "bundle_id": "bun-alpha-secret"},
    )
    assert priv_ret_b.status_code == 403

    # 6b. Tampered bundle payload must fail verification
    tampered_bundle = copy.deepcopy(bundle_on_c)
    tampered_bundle["okf_manifest"]["claims"][0]["statement"] = "TAMPERED CLAIM: 99.9% fidelity over 1000km"
    verify_tampered = node_c.post("/api/v1/trust/verify", json=tampered_bundle)
    assert verify_tampered.status_code == 200
    ver_report = verify_tampered.json()
    assert ver_report["status"] == "verification_failed"
    assert ver_report["integrity_verified"] is False
    assert ver_report["signature_verified"] is False

    # 6c. Offline peer resilience during federated discovery
    node_b.post(
        "/api/v1/federation/peers",
        json={
            "peer_node_id": "node-offline",
            "name": "Offline Peer Node",
            "endpoint": "http://node-offline.local:8099",
            "auto_approve": True,
        },
    )
    resilient_search = node_b.post(
        "/api/v1/search",
        json={"query": "entanglement", "scope": "federated"},
    )
    assert resilient_search.status_code == 200
    res_body = resilient_search.json()
    assert res_body["total"] >= 1
    peer_statuses = {p["peer_node_id"]: p["status"] for p in res_body["trace"]["peers_queried"]}
    assert peer_statuses.get("node-offline") == "unreachable"

