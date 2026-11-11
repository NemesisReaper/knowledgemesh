"""Comprehensive API integration, RBAC, agent credential, OKF, trust, and SDK tests."""

from __future__ import annotations

import json
import urllib.parse
from fastapi.testclient import TestClient

from knowmesh_api.main import app
from knowmesh_api.store import store
from sdk import KnowMeshClient, verify_bundle_signature

client = TestClient(app)


def setup_function() -> None:
    store._tables.clear()


def test_health_and_metrics() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["node_id"] == "node-a"

    m = client.get("/metrics")
    assert m.status_code == 200
    assert "http_requests_total" in m.text


def test_crud() -> None:
    r = client.post("/api/v1/bundles", json={"title": "Agent safety", "content": "Evidence"})
    assert r.status_code == 201
    key = r.json()["id"]
    assert client.get(f"/api/v1/bundles/{key}").json()["title"] == "Agent safety"
    assert client.delete(f"/api/v1/bundles/{key}").status_code == 204
    assert client.get(f"/api/v1/bundles/{key}").status_code == 404


def test_search() -> None:
    client.post("/api/v1/claims", json={"title": "Evidence grounded reasoning"})
    assert client.post("/api/v1/search", json={"query": "evidence"}).json()["total"] == 1


def test_auth_organizations_and_rbac_enforcement() -> None:
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@alpha.org",
            "password": "StrongPassword!123",
            "full_name": "Alice Architect",
            "organization_name": "Alpha Research Lab",
        },
    )
    assert reg.status_code == 201
    reg_data = reg.json()
    access_token = reg_data["access_token"]
    refresh_token = reg_data["refresh_token"]
    org_id = reg_data["organization"]["id"]

    # Wrong password rejected
    bad_login = client.post(
        "/api/v1/auth/login",
        json={"email": "alice@alpha.org", "password": "WrongPassword!999"},
    )
    assert bad_login.status_code == 401

    # Valid login & /auth/me
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "alice@alpha.org", "password": "StrongPassword!123"},
    )
    assert login.status_code == 200
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me.status_code == 200
    assert me.json()["role"] == "owner"

    # Refresh token rotates session
    ref = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert ref.status_code == 200
    assert "access_token" in ref.json()

    # Add a read-only member and verify backend RBAC blocks publishing
    add_mem = client.post(
        f"/api/v1/organizations/{org_id}/members",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": "viewer@alpha.org",
            "full_name": "Read Only Viewer",
            "role": "member",
            "password": "ViewerPassword!123",
        },
    )
    assert add_mem.status_code == 201
    viewer_login = client.post(
        "/api/v1/auth/login",
        json={"email": "viewer@alpha.org", "password": "ViewerPassword!123"},
    )
    viewer_token = viewer_login.json()["access_token"]

    denied_pub = client.post(
        "/api/v1/bundles",
        headers={"Authorization": f"Bearer {viewer_token}"},
        json={"title": "Unauthorized Bundle", "content": "Should be blocked by RBAC"},
    )
    assert denied_pub.status_code == 403

    # Logout revokes access token
    client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {viewer_token}"})
    revoked_check = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {viewer_token}"})
    assert revoked_check.status_code == 401


def test_agent_credentials_one_time_secret_and_least_privilege() -> None:
    # Register an agent with default least-privilege (read/search/verify only)
    ag_resp = client.post(
        "/api/v1/agents",
        json={
            "name": "DiscoveryBot",
            "description": "Read-only research agent",
            "permissions": ["knowledge:read", "knowledge:search", "verification:read"],
            "issue_initial_credential": True,
        },
    )
    assert ag_resp.status_code == 201
    ag_data = ag_resp.json()
    agent_id = ag_data["agent_id"]
    initial_cred = ag_data["initial_credential"]
    raw_secret = initial_cred["secret"]
    cred_id = initial_cred["credential_id"]
    assert raw_secret.startswith("km_live_")

    # Subsequent GET /credentials must NEVER expose the raw secret
    creds_list = client.get("/api/v1/credentials").json()["items"]
    assert len(creds_list) == 1
    assert "secret" not in creds_list[0]
    assert "secret_hash" not in creds_list[0]

    # Least privilege: agent cannot publish without knowledge:publish
    pub_denied = client.post(
        "/api/v1/bundles",
        headers={"X-KnowMesh-Key": raw_secret},
        json={"title": "Agent Attempted Publish", "content": "Denied"},
    )
    assert pub_denied.status_code == 403

    # Grant knowledge:publish and rotate credential
    upd = client.patch(
        f"/api/v1/agents/{agent_id}/permissions",
        json={"permissions": ["knowledge:read", "knowledge:search", "knowledge:publish", "verification:read"]},
    )
    assert upd.status_code == 200
    rotated = client.post(f"/api/v1/credentials/{cred_id}/rotate")
    assert rotated.status_code == 200
    new_secret = rotated.json()["secret"]

    # Old credential was revoked during rotation
    old_try = client.get("/api/v1/bundles", headers={"X-KnowMesh-Key": raw_secret})
    assert old_try.status_code == 401

    # New credential with updated permissions can publish
    pub_ok = client.post(
        "/api/v1/bundles",
        headers={"X-KnowMesh-Key": new_secret},
        json={
            "title": "Authorized Agent Knowledge Bundle",
            "description": "Published with rotated API key",
            "claims": [{"statement": "Ed25519 signatures ensure bundle authenticity."}],
            "evidence": [{"source_uri": "https://rfc-editor.org/rfc/rfc8032", "description": "RFC 8032 Ed25519"}],
        },
    )
    assert pub_ok.status_code == 201


def test_bundle_revisions_diff_provenance_graph_and_sdk_verification() -> None:
    # Publish v1
    v1_resp = client.post(
        "/api/v1/bundles",
        json={
            "bundle_id": "bun-climate-2026",
            "title": "Grid Carbon Intensity Baseline",
            "description": "Regional carbon intensity telemetry v1",
            "category": "energy",
            "version": "1.0.0",
            "claims": [
                {
                    "claim_id": "cl-grid-1",
                    "statement": "Solar generation peaked at 42% of grid mix in Q2.",
                    "status": "evidence_attached",
                    "evidence_ids": ["ev-grid-1"],
                }
            ],
            "evidence": [
                {
                    "evidence_id": "ev-grid-1",
                    "title": "ISO Telemetry Report Q2",
                    "source_uri": "https://grid.example.org/reports/q2",
                    "description": "Metered hourly generation dataset",
                }
            ],
        },
    )
    assert v1_resp.status_code == 201
    v1 = v1_resp.json()
    assert v1["verification"]["status"] == "verified"
    assert v1["verification"]["integrity_verified"] is True
    assert v1["verification"]["signature_verified"] is True

    # Evaluate claim lifecycle
    eval_resp = client.patch(
        "/api/v1/claims/cl-grid-1/status",
        json={"status": "supported", "reason": "Confirmed against primary telemetry"},
    )
    assert eval_resp.status_code == 200
    assert eval_resp.json()["status"] == "supported"

    # Publish v2 revision
    v2_resp = client.post(
        "/api/v1/bundles/bun-climate-2026/revisions",
        json={
            "version": "1.1.0",
            "description": "Regional carbon intensity telemetry v2 with Q3 update",
            "change_note": "Added Q3 battery storage claim",
            "claims": [
                {
                    "claim_id": "cl-grid-1",
                    "statement": "Solar generation peaked at 42% of grid mix in Q2.",
                    "status": "supported",
                    "evidence_ids": ["ev-grid-1"],
                },
                {
                    "claim_id": "cl-grid-2",
                    "statement": "Battery storage curtailed evening ramp emissions by 18% in Q3.",
                    "status": "supported",
                    "evidence_ids": ["ev-grid-1"],
                },
            ],
        },
    )
    assert v2_resp.status_code == 201
    v2 = v2_resp.json()
    assert v2["current_revision"] == "1.1.0"
    assert v2["previous_revision"] == "1.0.0"
    assert len(v2["revisions"]) == 2

    # Compare revisions
    diff = client.get("/api/v1/bundles/bun-climate-2026/diff?from_rev=1.0.0&to_rev=1.1.0").json()
    assert diff["changed"] is True
    assert len(diff["added_claims"]) == 1
    assert diff["added_claims"][0]["claim_id"] == "cl-grid-2"

    # Knowledge graph & provenance
    graph = client.get("/api/v1/bundles/bun-climate-2026/graph").json()
    assert graph["stats"]["node_count"] >= 3
    prov = client.get("/api/v1/bundles/bun-climate-2026/provenance").json()
    assert len(prov["provenance"]) >= 2

    # Verify via Python SDK against live app transport
    def sdk_transport(method: str, url: str, body, headers):
        parsed = urllib.parse.urlsplit(url)
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        resp = client.request(method, path, json=body, headers=headers)
        return resp.status_code, (resp.json() if resp.content else None)

    sdk_client = KnowMeshClient("http://testserver", transport=sdk_transport)
    ident = sdk_client.get_node_identity()
    fetched = sdk_client.get_bundle("bun-climate-2026")
    sig_check = verify_bundle_signature(fetched, public_key=ident["public_key"], raise_on_failure=True)
    assert sig_check["verified"] is True


def test_ssrf_peer_validation_and_key_rotation() -> None:
    # SSRF protection must block file:// and cloud metadata IPs
    bad_scheme = client.post(
        "/api/v1/federation/peers",
        json={"name": "File Peer", "endpoint": "file:///etc/passwd"},
    )
    assert bad_scheme.status_code == 422

    bad_metadata = client.post(
        "/api/v1/federation/peers",
        json={"name": "Metadata SSRF", "endpoint": "http://169.254.169.254/latest/meta-data"},
    )
    assert bad_metadata.status_code == 422

    # Node key rotation records revocation and issues new Ed25519 fingerprint
    old_ident = client.get("/api/v1/nodes/node-a/identity").json()
    rot = client.post("/api/v1/nodes/node-a/rotate-key?reason=security_drill")
    assert rot.status_code == 200
    new_ident = client.get("/api/v1/nodes/node-a/identity").json()
    assert new_ident["key_fingerprint"] != old_ident["key_fingerprint"]
    revocations = client.get("/api/v1/trust/revocations").json()["items"]
    assert len(revocations) >= 1
