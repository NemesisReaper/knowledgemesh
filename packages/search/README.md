# KnowMesh Search

A dependency-free Python search package for KnowMesh. It provides an in-memory
inverted index, BM25 lexical ranking, an optional caller-supplied semantic
encoder, reciprocal-rank fusion, and bounded retrieval-context assembly.

## Quick start

```python
from packages.search import DocumentRecord, SearchIndex, RetrievalService

index = SearchIndex()
index.upsert(DocumentRecord(
    id="claim-001",
    title="Federated agent knowledge",
    content="Agents publish and retrieve evidence-backed knowledge bundles.",
    bundle_id="bundle-001",
    publisher_id="node-a",
))

result = RetrievalService(index).retrieve("evidence-backed knowledge", limit=5)
for hit in result.hits:
    print(hit.document.id, hit.score)
print(result.context)
```

## Semantic adapter

Implement `encode(texts)` on your embedding provider, then pass it to
`SemanticIndex`. No model, network call, or embedding dependency is bundled.

## Scope and limitations

- Indexes are in-memory and must be rebuilt from persisted OKF/bundle records.
- Search scores are relevance estimates, not truth or trust scores.
- Semantic search requires a caller-provided embedding implementation.
- Hybrid search uses reciprocal-rank fusion; it does not compare raw BM25 and
  cosine scores directly.
- Retrieval returns untrusted source text. It does not neutralize prompt
  injection or establish claim validity.
- This package is a local search subsystem, not a federated search transport.
