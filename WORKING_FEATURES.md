# KnowMesh Working Features Inventory

All features listed below are implemented, connected to real persistence and domain packages, and verified by automated tests (`72 passed`).

## 1. Identity, Authentication & Multi-Tenant Organizations
- **User Registration & Login** (`POST /api/v1/auth/register`, `POST /api/v1/auth/login`): Passwords hashed with `scrypt` (random 16-byte salt); issues signed access and refresh tokens.
- **Session Refresh & Revocation** (`POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`): Rotates refresh tokens and revokes access token JTIs via `TokenRevocationStore`.
- **Organization & Member RBAC** (`POST /api/v1/organizations`, `POST /api/v1/organizations/{id}/members`): Supports `owner`, `administrator`, `curator`, `developer`, and `member` (read-only) roles enforced on the backend via FastAPI dependencies.

## 2. Independent Knowledge Nodes & Ed25519 Key Management
- **Node Registration** (`POST /api/v1/nodes`): Automatically generates an Ed25519 keypair (`packages/trust/identity.py`) and computes a SHA-256 key fingerprint.
- **Visibility Policies** (`PATCH /api/v1/nodes/{id}`): Enforces `private`, `organization`, and `federated` visibility scopes.
- **Key Rotation & Revocation** (`POST /api/v1/nodes/{id}/rotate-key`): Rotates the node's Ed25519 keypair, records the old fingerprint in `RevocationRegistry`, and appends a provenance event.

## 3. AI Agent Identity & One-Time API Credentials
- **Agent Registration** (`POST /api/v1/agents`): Associates agents with a node and organization using least-privilege default scopes (`knowledge:read`, `knowledge:search`, `verification:read`).
- **One-Time Secret Issuance** (`POST /api/v1/credentials`): Generates `km_live_...` secrets, stores only the SHA-256 hash at rest, and never returns the plaintext secret on subsequent `GET /api/v1/credentials` calls.
- **Credential Rotation & Revocation** (`POST /api/v1/credentials/{id}/rotate`, `POST /api/v1/credentials/{id}/revoke`).

## 4. OKF Knowledge Bundles, Claims, Evidence & Evolution
- **OKF Validation** (`POST /api/v1/okf/validate`): Validates manifests, claims, and evidence links for structural integrity and dangling references.
- **Signed Bundle Publication** (`POST /api/v1/bundles`): Computes canonical SHA-256 digest and Merkle root, signs with node's Ed25519 key, runs adversarial prompt-injection heuristics (`knowmesh_worker`), indexes in `BM25Ranker`, and records hash-chained provenance.
- **Immutable Revisions & Diffing** (`POST /api/v1/bundles/{id}/revisions`, `GET /api/v1/bundles/{id}/diff`): Preserves all historical revisions (`1.0.0`, `1.1.0`, ...) and computes structured diffs of added, removed, and modified claims.
- **Claim Lifecycle & Reasoning** (`PATCH /api/v1/claims/{id}/status`): Supports full lifecycle (`proposed` -> `evidence_attached` -> `under_review` -> `supported` / `contested` / `inconclusive` / `rejected` -> `superseded` / `archived`) backed by `packages/intelligence` and `packages/evaluation`.
- **Knowledge Graph Construction** (`GET /api/v1/bundles/{id}/graph`): Builds Document-Claim-Source graphs and computes density/node/edge statistics.

## 5. HTTP Federation Protocol, Discovery & Pull Synchronization
- **Peer Handshake & SSRF Protection** (`POST /api/v1/federation/peers`): Validates peer URLs against SSRF rules (blocking `file://`, loopback/link-local metadata IPs `169.254.169.254`) and verifies remote `/api/v1/federation/identity` Ed25519 fingerprints.
- **Federated Search** (`POST /api/v1/search` with `scope="federated"`): Queries local BM25 index and fans out to active approved peers with `CircuitBreaker` failure containment and execution trace reporting.
- **Verified Remote Bundle Retrieval** (`POST /api/v1/federation/retrieve`): Fetches remote bundles, recomputes canonical OKF digests, verifies Ed25519 signatures before persistence, and denies access (`403`) to `private` bundles.
- **Pull-Based Synchronization** (`POST /api/v1/federation/peers/{id}/sync`): Compares local and remote catalogs via `plan_sync`, pulls new and upstream-updated revisions while preserving previous revisions, and reports independent conflicts without silent overwrite.

## 6. Organization Console & Developer Platform
- **Next.js 14 + TypeScript Console (`apps/dashboard`)**: Dark-first enterprise control surface with Overview, Interactive SVG Network Topology Graph, 9-Tab Node Inspector, 5-Step OKF Publishing Wizard, Federated Discovery with Slide-Out Drawer, Agents & One-Time Key Modal, Federation Sync Console, Interactive Cryptographic Verifier, Audit Trail, Developer Portal, and RBAC Settings.
- **Python SDK (`packages/sdk`)**: `KnowMeshClient`, `publish_bundle`, `search_knowledge`, `verify_bundle_payload`, and `verify_bundle_signature`.

