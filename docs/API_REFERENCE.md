# KnowMesh API Reference (`v1`)

Base URL: `http://localhost:8000/api/v1`

Interactive OpenAPI documentation is available at `http://localhost:8000/docs` when the API server is running.

---

## 1. Authentication Headers

KnowMesh supports two authentication mechanisms:
1. **User Session JWT**:
   `Authorization: Bearer <access_token>`
2. **AI Agent API Key**:
   `X-API-Key: km_live_<secret>` (or `Authorization: Bearer km_live_<secret>`)

---

## 2. Core Endpoints

### 2.1 System & Demo Bootstrap
- `GET /health` — Liveness probe (`{"status": "ok"}`).
- `GET /api/v1/health` — Detailed subsystem health report (`database`, `federation`, `search`, `crypto`).
- `GET /api/v1/overview` — Aggregated counts, topology summary, and recent activity.
- `POST /api/v1/demo/bootstrap` — Seeds the 3-node multi-organization federation showcase (`Node A`, `Node B`, `Node C`) with signed bundles, claims, evidence, agents, and peer links.

### 2.2 Identity, Users & Organizations
- `POST /api/v1/auth/register` — Register a user account (`email`, `password`, `full_name`, optional `org_name`).
- `POST /api/v1/auth/login` — Authenticate and receive `access_token` + `refresh_token`.
- `POST /api/v1/auth/refresh` — Exchange a `refresh_token` for a new token pair.
- `POST /api/v1/auth/logout` — Revoke the active token (`jti`).
- `GET /api/v1/auth/me` — Inspect the current user or agent principal and memberships.
- `GET /api/v1/organizations` / `POST /api/v1/organizations` — List or create organizations.
- `GET /api/v1/organizations/{org_id}/members` / `POST /api/v1/organizations/{org_id}/members` — List or assign organization roles (`owner`, `admin`, `curator`, `developer`, `member`).

### 2.3 Independent Knowledge Nodes
- `GET /api/v1/nodes` — List registered knowledge nodes.
- `POST /api/v1/nodes` — Register a node and generate its Ed25519 keypair and DID.
- `GET /api/v1/nodes/{node_id}` / `PATCH /api/v1/nodes/{node_id}` — Inspect or update node visibility (`private`, `organization`, `federated`), status, or capabilities.
- `GET /api/v1/nodes/{node_id}/identity` — Public cryptographic identity card (DID, Ed25519 public key in hex/base64, capabilities).
- `GET /api/v1/nodes/{node_id}/health` — Node health check and peer reachability summary.

### 2.4 AI Agents & Credentials
- `GET /api/v1/agents` / `POST /api/v1/agents` — List or register AI agents with scoped permissions.
- `POST /api/v1/agents/{agent_id}/credentials` — Generate a new `km_live_...` API credential (returned once; stored as SHA-256 hash).
- `POST /api/v1/agents/{agent_id}/credentials/{credential_id}/rotate` — Atomically revoke an existing credential and issue a replacement.
- `DELETE /api/v1/agents/{agent_id}/credentials/{credential_id}` — Revoke an agent credential.

### 2.5 Knowledge Bundles, Revisions, Claims & Evidence
- `GET /api/v1/bundles` — List accessible knowledge bundles (filtered by `org_id`, `node_id`, `domain`, `visibility`, `status`).
- `POST /api/v1/bundles` — Validate, canonicalize (RFC 8785 JCS), sign (Ed25519), and publish a new OKF knowledge bundle.
- `GET /api/v1/bundles/{bundle_id}` — Retrieve full bundle envelope including OKF document, claims, evidence, provenance, and revision lineage.
- `POST /api/v1/bundles/{bundle_id}/revisions` — Publish a new immutable revision (`v2`, `v3`, ...) preserving parent-child lineage and superseding the prior revision.
- `POST /api/v1/bundles/{bundle_id}/status` — Archive or withdraw a bundle with a recorded reason.
- `GET /api/v1/bundles/{bundle_id}/verify` — Execute full cryptographic and provenance verification on a bundle (`digest_verified`, `signature_verified`, `signer_recognized`, `provenance_available`).
- `POST /api/v1/verify` — Verify an arbitrary or tampered bundle payload on demand.
- `GET /api/v1/claims` / `PATCH /api/v1/claims/{claim_id}/status` — List claims, inspect quality rubric scores, or transition claim review lifecycle status.
- `GET /api/v1/evidence` / `POST /api/v1/evidence` — List or attach traceable evidence records.

### 2.6 Federated Discovery, Search & Synchronization
- `POST /api/v1/search` — Execute local, federated, or hybrid search with BM25 ranking, filters, verification status badges, and per-node search trace telemetry.
- `POST /api/v1/discovery/search` — Federated peer discovery endpoint.
- `GET /api/v1/federation/peers` / `POST /api/v1/federation/peers` — List or register federated peer nodes.
- `POST /api/v1/federation/peers/{peer_id}/sync` — Run pull-based synchronization with a peer, verifying digests and signatures and reporting synced, skipped, or conflicted bundles.
- `GET /api/v1/federation/protocol/manifest` — Public federated bundle manifest for pull synchronization.
- `GET /api/v1/federation/protocol/bundles/{bundle_id}` — Public federated bundle retrieval (enforces `visibility == "federated"`).

### 2.7 Lineage, Graph, Reputation & Audit
- `GET /api/v1/evolution/lineage/{bundle_id}` — Retrieve full `knowledge_dna` lineage tree and revision diffs.
- `GET /api/v1/graph` — Export knowledge graph entities and edges (`claims`, `evidence`, `sources`, `nodes`).
- `GET /api/v1/reputation` — Inspect node and contributor reputation profiles and trust scores.
- `GET /api/v1/audit` — Query immutable security and operational audit trail events.

