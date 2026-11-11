# KnowMesh System Architecture

## 1. High-Level Architecture

```mermaid
flowchart TB
    subgraph Console["Next.js Organization Console & Developer Portal (apps/dashboard)"]
        UI_Overview["Overview & Topology Graph"]
        UI_Nodes["My Nodes (9-Tab Inspector)"]
        UI_Knowledge["Knowledge & 5-Step OKF Wizard"]
        UI_Discover["Federated Search & Drawer"]
        UI_Trust["Cryptographic Verifier & RBAC"]
    end

    subgraph SDK["Python Agent SDK (packages/sdk)"]
        AgentClient["KnowMeshClient + verify_bundle_signature"]
    end

    subgraph NodeA["KnowMesh Node A (apps/api)"]
        FastAPI["FastAPI v1 Router & Auth/RBAC Dependencies"]
        Service["KnowMeshService Domain Orchestrator"]
        DB_A[("PostgreSQL / SQLite Persistence")]
    end

    subgraph DomainPackages["Integrated Domain Packages (packages/*)"]
        OKF["okf: Manifest, Validator, Canonical Hash, Merkle Root"]
        Trust["trust: Ed25519 Keys, Signatures, Provenance Chain, Revocation"]
        Search["search: BM25 Ranker & Hybrid Search Index"]
        Fed["federation: PeerRegistry, CircuitBreaker, SyncPlanner"]
        DNA["knowledge_dna: Revision History & Lineage Graph"]
        Graph["knowledge_graph: Document-Claim-Source Graph"]
        Intel["intelligence & evaluation: Claim Reasoning & Quality Rubric"]
        Worker["knowmesh_worker: Extraction, Evolution, Decay, Adversarial Scan"]
    end

    subgraph PeerNodes["Independent Federated Peers"]
        NodeB["KnowMesh Node B (Independent DB & Ed25519 Key)"]
        NodeC["KnowMesh Node C (Independent DB & Ed25519 Key)"]
    end

    Console -->|REST + Bearer Token| FastAPI
    SDK -->|REST + X-KnowMesh-Key| FastAPI
    FastAPI --> Service
    Service --> DB_A
    Service --> DomainPackages
    Service <-->|HTTP Federation Protocol| NodeB
    Service <-->|HTTP Federation Protocol| NodeC
```

---

## 2. Persistence Schema (`packages/knowledge`)

The SQLAlchemy 2.0 schema in `packages/knowledge/src/knowmesh_knowledge/models/enterprise.py` persists:

1. **Identity & Multi-Tenancy**: `organizations`, `users`, `memberships`
2. **Independent Nodes & Cryptography**: `nodes`, `node_keys` (Ed25519 public/private keys, fingerprints, rotation & revocation state)
3. **AI Agents & Credentials**: `agents`, `credentials` (SHA-256 secret hashes, prefixes, scopes, expiration, revocation)
4. **OKF Knowledge & Immutable Revisions**: `knowledge_collections`, `knowledge_bundles`, `knowledge_revisions` (canonical digest, Merkle root, Ed25519 signature envelope, full OKF manifest), `claim_records`, `evidence_records`
5. **Provenance & Federation**: `provenance_events` (hash-chained records), `peer_connections`, `peer_capabilities`, `sync_records`
6. **Governance & Operations**: `access_policies`, `audit_events`, `background_jobs`

---

## 3. Cryptographic Signing & Verification Pipeline

1. **Canonicalization**: When a knowledge bundle is published, `OKFManifest.canonical_payload()` extracts the canonical fields (`bundle_id`, `title`, `version`, `format_version`, `publisher_id`, `description`, `claims`, `evidence`, `links`, `metadata`) and serializes them deterministically with sorted keys and UTF-8 encoding (`packages/okf/hashing.py`).
2. **Digest & Merkle Root**: A deterministic `sha256:<hex>` content digest and a Merkle root over claim/evidence leaves are computed.
3. **Ed25519 Signing**: `sign_object` (`packages/trust/signing.py`) signs `knowmesh-okf-bundle:<canonical_bytes>` using the publishing node's active Ed25519 keypair.
4. **Verification on Retrieval**: Both local inspection and remote peer retrieval (`retrieve_remote_bundle`) recompute the canonical OKF digest and verify the Ed25519 signature against the signer's public key before accepting or storing a revision. Tampered payloads are rejected immediately.

