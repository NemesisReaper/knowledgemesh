# KnowMesh Knowledge Graph

An in-memory graph subsystem for representing relationships among claims,
concepts, documents, sources, agents and experiments.

## Modules

- `models.py`: typed graph nodes/edges and thread-safe graph container.
- `builder.py`: construct graph from documents, claims, evidence and relations.
- `queries.py`: typed filters and bounded neighborhood queries.
- `traversal.py`: BFS, DFS, weighted shortest path and bounded simple paths.
- `engine.py`: graph statistics, neighborhood/path helpers, snapshots and diffs.

## Quick start

```python
from packages.knowledge_graph import (
    GraphBuilder, KnowledgeGraphEngine, breadth_first,
)

report = GraphBuilder().build(
    claims=[
        {"id": "c1", "text": "Claim about federated knowledge"},
        {"id": "c2", "text": "Claim about evidence provenance"},
    ],
    evidence=[
        {"id": "e1", "title": "Research paper", "claim_id": "c1"},
    ],
    relations=[
        {"source": "claim:c1", "target": "claim:c2",
         "type": "related_to", "weight": 1.0},
    ],
)
engine = KnowledgeGraphEngine(report.graph)
print(engine.stats())
print(breadth_first(report.graph, "claim:c1", direction="both"))
```

## Data model

Nodes and edges have stable IDs, typed labels and arbitrary metadata.
Edges are directed by default; set `directed=False` for undirected links.
Supported edge types include `supports`, `contradicts`, `derived_from`,
`references`, `related_to`, `instance_of`, `part_of`, `caused_by`,
`supersedes` and `published_by`.

## Limitations

- Storage is in-memory. It is not Neo4j, a graph database, or a persistence
  layer; persist source records and rebuild or add a database adapter.
- It does not infer relations automatically or perform entity resolution.
- The builder uses a simple mapping contract and does not claim conformance
  to an external OKF schema.
- Graph edges encode relationships, not truth. Trust and claim verification
  must remain separate from graph topology.
- Traversal is bounded where paths may grow combinatorially.
