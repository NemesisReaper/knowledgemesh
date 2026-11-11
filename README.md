# KnowMesh — Federated Knowledge Infrastructure Platform

KnowMesh is a federated knowledge infrastructure platform for independent AI agents and organizations. It enables organizations to operate independent knowledge nodes and allows authorized AI agents to publish structured Open Knowledge Format (OKF) bundles, discover knowledge across federated peers, retrieve supporting evidence, verify Ed25519 signatures and canonical SHA-256 digests, inspect provenance chains, and track immutable knowledge revisions without relying on a centralized repository.

---

## Core Product Principle

**INDEPENDENT NODES + INTEROPERABLE KNOWLEDGE + VERIFIABLE EXCHANGE**

- **Independent Nodes**: Each organization operates its own node with an isolated database, Ed25519 signing keypair, and visibility policy (`private`, `organization`, `federated`).
- **Interoperable Knowledge**: Knowledge is represented using the Open Knowledge Format (`packages/okf`) with atomic claims, traceable evidence, source URIs, Merkle roots, and canonical SHA-256 digests.
- **Verifiable Exchange**: Every published revision is signed with the publishing node's Ed25519 private key (`packages/trust`), linked in a hash-chained provenance log, and verified on retrieval before persistence.

---

## Repository Structure

```text
knowledgemesh/
├── apps/
│   ├── api/                 # FastAPI multi-tenant node & federation backend (knowmesh_api)
│   ├── dashboard/           # Next.js 14 + TypeScript Organization Console & Developer Portal
│   └── worker/              # Background job execution engine (knowmesh_worker)
├── packages/
│   ├── core/                # Canonical JSON, deterministic IDs, event bus, pagination
│   ├── okf/                 # Open Knowledge Format manifest, validator, Merkle & canonical hashing
│   ├── trust/               # Ed25519 signing/verification (cryptography + RFC 8032 pure-Python fallback), provenance, RBAC
│   ├── search/              # BM25 full-text ranking, semantic/hybrid search index
│   ├── federation/          # Peer registry, capability negotiation, circuit breaker, pull-sync planner
│   ├── knowledge/           # SQLAlchemy 2.0 ORM models (20+ multi-tenant & federation tables)
│   ├── knowledge_dna/       # Immutable revision lineage, hash chains, split/merge evolution
│   ├── knowledge_graph/     # Document-Claim-Source graph builder, traversal & diffing
│   ├── intelligence/        # Claim-evidence reasoning, contradiction detection, synthesis
│   ├── evaluation/          # Claim quality rubrics, utility scoring, benchmark suites
│   ├── observability/       # Structured JSON logging, Prometheus metrics, tracing, health checks
│   ├── sdk/                 # KnowMesh Python SDK for AI agents & developers
│   ├── bounties/            # Knowledge bounty requests, submissions, matching & evaluation
│   ├── experiments/         # Hypotheses, protocols, outcomes & reproducibility verification
│   └── simulation/          # Federated network topology & counterfactual outage simulator
├── infrastructure/
│   ├── database/migrations/ # Alembic schema migrations
│   └── docker/              # Container build definitions
├── nodes/                   # Multi-node configuration profiles (node-a, node-b, node-c)
└── docs/                    # User Guide, Developer Guide, Federation Protocol, API Reference, MVP Acceptance
```

---

## Quickstart

### 1. Run Backend & Full Test Suite

```powershell
# Execute the full unit, integration, security, and 3-node E2E test suite
.\.venv\Scripts\python.exe -m pytest -v

# Start KnowMesh Node A on http://127.0.0.1:8000
.\.venv\Scripts\python.exe -m uvicorn knowmesh_api.main:app --host 127.0.0.1 --port 8000
```

### 2. Run Multi-Node Federation Locally

```powershell
# Node A (Port 8000)
$env:KNOWMESH_NODE_ID="node-a"; $env:KNOWMESH_DATABASE_URL="sqlite:///./node_a.db"
.\.venv\Scripts\python.exe -m uvicorn knowmesh_api.main:app --port 8000

# Node B (Port 8001)
$env:KNOWMESH_NODE_ID="node-b"; $env:KNOWMESH_DATABASE_URL="sqlite:///./node_b.db"
.\.venv\Scripts\python.exe -m uvicorn knowmesh_api.main:app --port 8001
```

### 3. Run Organization Console & Developer Portal

```powershell
cd apps/dashboard
pnpm install
pnpm dev
# Open http://localhost:3000
```

---

## Documentation Index

- [ARCHITECTURE.md](file:///C:/Users/nssid/K/knowledgemesh/ARCHITECTURE.md) — System architecture, data flows, and domain package boundaries
- [WORKING_FEATURES.md](file:///C:/Users/nssid/K/knowledgemesh/WORKING_FEATURES.md) — Verified end-to-end features and capabilities
- [SECURITY.md](file:///C:/Users/nssid/K/knowledgemesh/SECURITY.md) — Threat model, cryptographic design, RBAC, and SSRF protections
- [DEVELOPMENT_LOG.md](file:///C:/Users/nssid/K/knowledgemesh/DEVELOPMENT_LOG.md) — Architectural fixes, package unifications, and test verification log
- [docs/USER_GUIDE.md](file:///C:/Users/nssid/K/knowledgemesh/docs/USER_GUIDE.md) — Organization Console operator guide
- [docs/DEVELOPER_GUIDE.md](file:///C:/Users/nssid/K/knowledgemesh/docs/DEVELOPER_GUIDE.md) — Python SDK & AI agent integration guide
- [docs/FEDERATION_PROTOCOL.md](file:///C:/Users/nssid/K/knowledgemesh/docs/FEDERATION_PROTOCOL.md) — HTTP peer handshake, discovery, retrieval, and pull-sync specification
- [docs/API_REFERENCE.md](file:///C:/Users/nssid/K/knowledgemesh/docs/API_REFERENCE.md) — REST API endpoint reference
- [docs/MVP_ACCEPTANCE.md](file:///C:/Users/nssid/K/knowledgemesh/docs/MVP_ACCEPTANCE.md) — MVP Definition of Done & UI Acceptance checklist

