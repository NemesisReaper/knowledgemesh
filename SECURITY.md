# KnowMesh Security Architecture & Threat Model

## 1. Core Security Principles

1. **Knowledge Content is Untrusted Data**: Retrieved knowledge bundles, claims, and evidence are treated strictly as untrusted data and are never executed as code, shell commands, SQL, or system instructions. Adversarial prompt-injection heuristics (`knowmesh_worker/jobs/adversarial_review.py`) scan published text and flag suspicious instruction-override patterns.
2. **Epistemic Separation**: Cryptographic verification (`integrity_verified`, `signature_verified`, `signer_recognized`) proves publisher authenticity and payload integrity. It is never conflated with factual truth (`supported`, `contested`, `inconclusive`, `rejected`).
3. **Least Privilege & Backend RBAC**: All role and agent permission checks are enforced on the backend (`apps/api/src/knowmesh_api/dependencies.py` and `security.py`).

## 2. Credential & Key Security

- **Password Hashing**: User passwords are hashed using `hashlib.scrypt` (`N=16384, r=8, p=1`) with a 16-byte CSPRNG salt and verified in constant time via `hmac.compare_digest`.
- **One-Time Agent API Keys**: Agent credentials (`km_live_...`) are generated with 192 bits of entropy (`secrets.token_urlsafe(24)`). Only the `key_prefix` and SHA-256 `secret_hash` are stored in the database. Plaintext secrets are returned once upon creation/rotation and never returned again.
- **Ed25519 Node Signing Keys**: Each node signs canonical OKF payloads with Ed25519 (`RFC 8032`). Public identity endpoints (`/api/v1/nodes/{id}/identity` and `/api/v1/federation/identity`) never expose private key material.

## 3. Federation & SSRF Protections

- **SSRF Validation (`validate_peer_endpoint`)**: Peer endpoints must use `http` or `https`, cannot contain embedded credentials, and block cloud metadata / link-local / multicast / unspecified addresses (`169.254.169.254`, `metadata.google.internal`, `0.0.0.0`, `169.254.0.0/16`).
- **Pre-Persistence Cryptographic Verification**: When a node retrieves a bundle from a federated peer (`retrieve_remote_bundle`), it recomputes the canonical OKF SHA-256 digest and verifies the Ed25519 signature envelope before storing the bundle. Any tampered payload is rejected immediately.
- **Private Knowledge Isolation**: Bundles with `visibility="private"` or `visibility="organization"` are excluded from federated catalogs, excluded from federated discovery (`POST /api/v1/federation/discover`), and blocked with `403 Forbidden` on `/api/v1/federation/bundles/{id}`.

