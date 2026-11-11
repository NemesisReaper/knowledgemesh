# KnowMesh Federation Protocol Specification (`knowmesh-fed/1.0`)

KnowMesh nodes exchange structured knowledge over an explicit, pull-based HTTP/JSON protocol with Ed25519 cryptographic signing and RFC 8785 JSON Canonicalization Scheme (JCS) digests.

---

## 1. Core Design Principles

1. **Sovereign Node Identity**: Every node generates an Ed25519 keypair and publishes its public key (`public_key_hex`, `public_key_b64`) and decentralized identifier (`did:knowmesh:<slug>-<fingerprint>`). Private keys never leave the node's key store.
2. **Canonical Content Addressing**: Knowledge bundles are represented as Open Knowledge Format (`OKFBundle`) documents. Content digests are computed over RFC 8785 canonical JSON (`packages/okf/hashing.py`) with volatile signature headers stripped prior to hashing.
3. **Explicit Visibility Enforcement**:
   - `private`: Never exposed in federated manifests, discovery endpoints, or remote bundle fetches.
   - `organization`: Restricted to authenticated principals within the owning organization.
   - `federated`: Exposed to authorized federated peers.
4. **Pull-Based Synchronization & Conflict Preservation**: Peers pull manifest deltas, verify digests and Ed25519 signatures before ingestion, retain historical revisions, and surface divergent lineage branches as explicit conflicts rather than silently overwriting data.

---

## 2. Canonical Signing Payload

When a node signs a knowledge bundle revision:

1. **OKF Content Digest (`content_digest`)**:
   - Constructed from the canonical OKF document fields (`title`, `summary`, `domain`, `claims`, `evidence`, `sources`, `tags`) serialized via deterministic RFC 8785 JCS (`canonicalize_json`) and hashed with `SHA-256` (`64`-character lowercase hex).
2. **Signed Envelope Message**:
   - Exact UTF-8 byte string:
     ```text
     {bundle_id}:{revision_number}:{content_digest}
     ```
3. **Ed25519 Signature (`signature`)**:
   - 64-byte Ed25519 signature over the UTF-8 message above, encoded as 128-character lowercase hex (`packages/trust/signing.py`).

---

## 3. Federation HTTP Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/nodes/{node_id}/identity` | `GET` | Returns node DID, Ed25519 public key (`hex` and `base64`), capabilities, and visibility mode. |
| `/api/v1/federation/protocol/manifest` | `GET` | Returns the node's federated manifest: node identity, protocol version (`knowmesh-fed/1.0`), and revision metadata (`bundle_id`, `revision_id`, `revision_number`, `content_digest`, `signature`, `signer_public_key`, `updated_at`) for all `federated` + `published` bundles. |
| `/api/v1/federation/protocol/bundles/{bundle_id}` | `GET` | Retrieves the full signed bundle envelope (`okf_document`, `claims`, `evidence`, `provenance`, `signature`, `content_digest`) if and only if the bundle visibility is `federated` (returns `403 Forbidden` for `private` or `organization` bundles). |
| `/api/v1/federation/peers` | `POST` | Registers a remote peer after SSRF validation (`packages/federation/peers.py`) and optional handshake inspection. |
| `/api/v1/federation/peers/{peer_id}/sync` | `POST` | Executes a pull-based synchronization cycle against a peer (`packages/federation/sync.py`), verifying every remote bundle's digest and Ed25519 signature before storing it locally. |
| `/api/v1/discovery/search` | `POST` | Queries local BM25/FTS index and fans out across active federated peers, merging and ranking results while reporting per-peer trace telemetry (`responded`, `unreachable`, latency). |

---

## 4. Resilience & Security Controls

- **SSRF Protection**: Peer endpoint URLs are validated by `validate_endpoint_url` in `packages/federation/peers.py`, blocking link-local metadata addresses (`169.254.169.254`), unspecified addresses (`0.0.0.0`), non-HTTP schemes, and loopback targets when `allow_private_endpoints=False`.
- **Circuit Breaker & Graceful Degradation**: Federated discovery records per-peer failures and timeouts without failing the overall search request. Unreachable peers are reported in `search_trace.peers` with `"status": "unreachable"`.
- **Tamper Rejection**: During peer synchronization or client-side verification, if a bundle's recomputed SHA-256 content digest or Ed25519 signature does not match, ingestion is rejected and recorded as a verification failure.

