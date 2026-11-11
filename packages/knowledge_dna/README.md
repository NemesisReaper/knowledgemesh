# KnowMesh Knowledge DNA

Knowledge DNA provides primitives for tracking the identity and evolution of knowledge artifacts:
content fingerprints, explicit mutations, splits, merges, lineage events, and revision history.

## Modules
- `identity.py`: stable logical identity and content fingerprint (not the same thing).
- `mutations.py`: explicit set/remove/append/increment/merge operations.
- `splits.py`: partition a list-valued field into child artifacts without changing the parent.
- `merges.py`: recursive merge with explicit conflict policy.
- `lineage.py`: append-only event graph with parent references.
- `history.py`: in-memory revision snapshots linked by SHA-256 fingerprints.

## Quick start
```python
from knowledge_dna import (
    KnowledgeHistory, Mutation, MutationKind, apply_mutation,
    split_knowledge, merge_knowledge,
)

history = KnowledgeHistory("claim-42")
history.record({"text": "A", "tags": ["x", "y"]}, actor="publisher")
updated = apply_mutation(
    {"text": "A", "confidence": 0.5},
    Mutation(MutationKind.INCREMENT, ("confidence",), 0.1, reason="new evidence"),
)
assert updated.payload["confidence"] == 0.6
assert history.verify()
```

## Important boundaries
- A fingerprint identifies bytes under this package's JSON encoding; it does not prove truth,
  authorship, or trust.
- This is a local in-memory reference implementation, not a distributed version-control system.
- History hash links are tamper-evident only while a trusted head is retained externally.
- Split/merge operations do not infer semantic equivalence or resolve epistemic disagreement.
- The package's payload contract is generic JSON-compatible mappings, not a claim of full OKF conformance.
- Canonical JSON here is deterministic for ordinary JSON values but is not RFC 8785/JCS.
