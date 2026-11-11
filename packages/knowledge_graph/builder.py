"""Build a graph from portable document and claim-like mappings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping
import hashlib
import json

from .models import (
    EdgeType, GraphEdge, GraphNode, KnowledgeGraph, NodeType,
)


@dataclass(frozen=True, slots=True)
class BuildReport:
    graph: KnowledgeGraph
    nodes_created: int
    edges_created: int
    warnings: tuple[str, ...] = ()


class GraphBuilder:
    """Convert normalized knowledge records into graph nodes and edges.

    Expected record shapes are intentionally permissive:
      - documents: {id, title, ...}
      - claims: {id, text/title, ...}
      - evidence: {id, claim_id, source_id, ...}
      - relations: {id?, source, target, type?, weight?}
    """
    def __init__(self) -> None:
        self.graph = KnowledgeGraph()
        self._warnings: list[str] = []

    @staticmethod
    def _stable_id(prefix: str, value: Any) -> str:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
        return f"{prefix}:{hashlib.sha256(raw.encode()).hexdigest()[:20]}"

    def add_document(self, record: Mapping[str, Any]) -> GraphNode:
        doc_id = str(record.get("id") or "")
        if not doc_id:
            raise ValueError("document requires id")
        node = GraphNode(
            id=f"document:{doc_id}", node_type=NodeType.DOCUMENT,
            label=str(record.get("title") or doc_id),
            properties={k: v for k, v in record.items() if k not in {"id", "title"}},
        )
        self.graph.add_node(node)
        return node

    def add_claim(self, record: Mapping[str, Any]) -> GraphNode:
        claim_id = str(record.get("id") or "")
        if not claim_id:
            raise ValueError("claim requires id")
        node = GraphNode(
            id=f"claim:{claim_id}", node_type=NodeType.CLAIM,
            label=str(record.get("text") or record.get("title") or claim_id),
            properties={k: v for k, v in record.items() if k not in {"id", "text", "title"}},
        )
        self.graph.add_node(node)
        return node

    def add_evidence(self, record: Mapping[str, Any]) -> GraphNode:
        evidence_id = str(record.get("id") or "")
        if not evidence_id:
            raise ValueError("evidence requires id")
        node = GraphNode(
            id=f"source:{evidence_id}", node_type=NodeType.SOURCE,
            label=str(record.get("title") or record.get("uri") or evidence_id),
            properties={k: v for k, v in record.items() if k not in {"id", "title"}},
        )
        self.graph.add_node(node)
        claim_id = record.get("claim_id")
        if claim_id:
            target = f"claim:{claim_id}"
            if self.graph.get_node(target):
                self.graph.add_edge(GraphEdge(
                    self._stable_id("edge", [node.id, target, "supports"]),
                    node.id, target, EdgeType.SUPPORTS,
                ))
            else:
                self._warnings.append(f"evidence {evidence_id} references missing claim {claim_id}")
        return node

    def add_relation(self, record: Mapping[str, Any]) -> GraphEdge | None:
        source, target = str(record.get("source") or ""), str(record.get("target") or "")
        if not source or not target:
            raise ValueError("relation requires source and target")
        if self.graph.get_node(source) is None or self.graph.get_node(target) is None:
            self._warnings.append(f"relation skipped; missing endpoint: {source} -> {target}")
            return None
        edge_type = EdgeType(record.get("type", EdgeType.RELATED_TO.value))
        edge_id = str(record.get("id") or self._stable_id("edge", [source, target, edge_type.value]))
        edge = GraphEdge(edge_id, source, target, edge_type,
                         float(record.get("weight", 1.0)),
                         {k: v for k, v in record.items()
                          if k not in {"id", "source", "target", "type", "weight"}},
                         bool(record.get("directed", True)))
        self.graph.add_edge(edge)
        return edge

    def build(self, *, documents: Iterable[Mapping[str, Any]] = (),
              claims: Iterable[Mapping[str, Any]] = (),
              evidence: Iterable[Mapping[str, Any]] = (),
              relations: Iterable[Mapping[str, Any]] = ()) -> BuildReport:
        for item in documents:
            self.add_document(item)
        for item in claims:
            self.add_claim(item)
        for item in evidence:
            self.add_evidence(item)
        for item in relations:
            self.add_relation(item)
        errors = self.graph.validate()
        if errors:
            raise ValueError("built graph is invalid: " + "; ".join(errors))
        return BuildReport(self.graph, len(self.graph.nodes()),
                           len(self.graph.edges()), tuple(self._warnings))


def build_graph(**records) -> BuildReport:
    return GraphBuilder().build(**records)
