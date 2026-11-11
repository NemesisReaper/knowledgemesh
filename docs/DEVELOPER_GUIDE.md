# KnowMesh Developer Guide & Python SDK

The **KnowMesh Developer Platform** enables engineers to connect independent AI agents and services to KnowMesh nodes using standard HTTP APIs or the `knowmesh_sdk` Python package.

---

## 1. Installation & Environment Setup

Inside the repository virtual environment (`C:\Users\nssid\K\knowledgemesh\.venv`), all domain packages and `packages/sdk` are pre-wired on `PYTHONPATH`.

To install `knowmesh-sdk` in editable mode in another environment:

```bash
pip install -e packages/okf -e packages/trust -e packages/sdk
```

---

## 2. Obtaining Agent API Credentials

1. Sign in to the KnowMesh Console or call `POST /api/v1/auth/login`.
2. Register an AI agent with least-privilege scopes:

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "org_id": "<ORG_ID>",
    "node_id": "<NODE_ID>",
    "name": "research-synthesizer-agent",
    "description": "Queries verified federated claims and publishes synthesis bundles",
    "permissions": [
      "knowledge:read",
      "knowledge:search",
      "knowledge:publish",
      "federation:discover",
      "verification:read"
    ]
  }'
```

3. Issue an API credential:

```bash
curl -X POST http://localhost:8000/api/v1/agents/<AGENT_ID>/credentials \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"label": "prod-agent-key", "expires_in_days": 90}'
```

Save the returned `api_key` (`km_live_...`) immediately. It is hashed with SHA-256 at rest and is never returned again.

---

## 3. Using the Python SDK (`packages/sdk`)

### 3.1 Connecting & Searching Federated Knowledge

```python
from packages.sdk import KnowMeshClient

client = KnowMeshClient(
    base_url="http://localhost:8000",
    api_key="km_live_your_agent_secret_key",
    timeout=10.0,
    max_retries=2,
)

# Check node health
health = client.health()
print("Node status:", health["status"])

# Execute federated search across authorized peers
results = client.search(
    query="transformer attention scaling",
    scope="federated",
    domain="machine-learning",
    limit=10,
)

for hit in results["results"]:
    print(f"[{hit['verification_status']}] {hit['title']} (rev {hit['revision_number']}) - score={hit['score']:.3f}")
```

### 3.2 Retrieving & Cryptographically Verifying a Bundle

Never equate retrieval with authenticity—always verify the canonical SHA-256 content digest and Ed25519 signature on the client side using `verify_bundle_signature`:

```python
from packages.sdk import KnowMeshClient, verify_bundle_signature

client = KnowMeshClient(base_url="http://localhost:8000", api_key="km_live_...")

bundle = client.get_bundle("bundle-id-here")

# Server-side verification endpoint
server_verification = client.verify_bundle(bundle["bundle_id"])
assert server_verification["overall_status"] == "verified"

# Zero-trust client-side cryptographic verification (RFC 8785 JCS SHA-256 + Ed25519)
client_verification = verify_bundle_signature(bundle)
assert client_verification.is_valid
assert client_verification.digest_valid
assert client_verification.signature_valid
print("Verified signer DID:", client_verification.signer_did)
```

### 3.3 Publishing a Signed Knowledge Bundle via SDK

If your agent holds the `knowledge:publish` permission, it can publish structured OKF bundles directly:

```python
published = client.publish_bundle({
    "org_id": "<ORG_ID>",
    "node_id": "<NODE_ID>",
    "title": "Benchmark Evaluation of Sparse Mixture-of-Experts Routing",
    "summary": "Empirical throughput and perplexity measurements across 8xH100 clusters.",
    "domain": "machine-learning",
    "visibility": "federated",
    "tags": ["moe", "routing", "benchmarks"],
    "claims": [
        {
            "statement": "Token-choice routing with capacity factor 1.25 reduces dropped tokens by 41% under skewed batch distributions.",
            "claim_type": "empirical",
            "confidence": 0.93,
            "tags": ["moe", "throughput"]
        }
    ],
    "evidence": [
        {
            "title": "Cluster Telemetry Run #402",
            "content": "Measured over 50B tokens on FineWeb-Edu validation split; p99 latency 18.4ms.",
            "evidence_type": "experiment",
            "source_uri": "https://metrics.example.org/runs/402",
            "reliability_score": 0.95,
            "direction": "supports"
        }
    ]
})
print("Published bundle ID:", published["bundle_id"], "Digest:", published["content_digest"])
```

