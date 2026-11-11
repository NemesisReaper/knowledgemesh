# KnowMesh Trust

Python trust primitives for node identity, Ed25519 signatures, artifact
verification, revocation, provenance, access control and policy evaluation.

## Install

```bash
pip install "cryptography>=42"
```

## Quick start

```python
from packages.trust import (
    generate_keypair, sign_object, verify_artifact,
    ProvenanceChain, ProvenanceAction,
)

keys = generate_keypair("node-a")
artifact = {"id": "bundle-1", "title": "Federated knowledge"}
signature = sign_object(artifact, keys)

result = verify_artifact(
    artifact, signature, {keys.identity.id: keys.identity}
)
assert result.verified

chain = ProvenanceChain("bundle-1")
chain.add(record_id="event-1", action=ProvenanceAction.CREATED,
          actor_id="node-a")
assert chain.verify()
```

## Security boundaries

- Ed25519 signatures prove possession of a private key for the signed bytes;
  they do not prove that a claim is true or that the key owner is trustworthy.
- Trust policy evaluation is separate from signature verification.
- Revocation and provenance registries are in-memory primitives. Production
  deployments must persist, authenticate, replicate and audit them.
- Private keys are exported as raw base64url bytes by `KeyPair`; protect them
  with a secret manager or encrypted keystore. Never commit them to source.
- `canonical_json_bytes` is a project-local deterministic JSON encoding, not
  a certified RFC 8785/JCS implementation. Use a specified cross-language
  canonicalization standard before interoperable production signing.
- The access-control engine is a local policy primitive, not a complete
  authorization server. Integrate it with authenticated principals and
  enforce checks at every API boundary.
- Provenance hash chains are tamper-evident only relative to a trusted,
  externally anchored chain head; they are not blockchain.
