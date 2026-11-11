"""High-level graph operations, statistics, diffing and snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import GraphEdge, GraphNode, KnowledgeGraph, NodeType, EdgeType
from .traversal import breadth_first, shortest_path


@dataclass(frozen=True, slots=True)
class GraphStats:
    node_count: int
    edge_count: int
    node_counts_by_type: dict[str, int]
    edge_counts_by_type: dict[str, int]
    density: float
    generation: int


@dataclass(frozen=True, slots=True)
class GraphDiff:
    added_nodes: tuple[str, ...]
    removed_nodes: tuple[str, ...]
    changed_nodes: tuple[str, ...]
    added_edges: tuple[str, ...]
    removed_edges: tuple[str, ...]
    changed_edges: tuple[str, ...]


class KnowledgeGraphEngine:
    def __init__(self, graph: KnowledgeGraph | None = None) -> None:
        self.graph = graph or KnowledgeGraph()

    def stats(self) -> GraphStats:
        nodes, edges = self.graph.nodes(), self.graph.edges()
        node_counts = {kind.value: sum(n.node_type == kind for n in nodes) for kind in NodeType}
        edge_counts = {kind.value: sum(e.edge_type == kind for e in edges) for kind in EdgeType}
        n = len(nodes)
        density = len(edges) / (n * (n - 1)) if n > 1 else 0.0
        return GraphStats(len(nodes), len(edges), node_counts, edge_counts,
                          density, self.graph.generation)

    def neighborhood(self, node_id: str, *, depth: int = 1,
                     direction: str = "both", limit: int = 1000):
        return breadth_first(self.graph, node_id, direction=direction,
                             max_depth=depth, limit=limit)

    def path(self, source: str, target: str, *, direction: str = "out"):
        return shortest_path(self.graph, source, target, direction=direction)

    def diff(self, other: KnowledgeGraph) -> GraphDiff:
        left_nodes = {n.id: n for n in self.graph.nodes()}
        right_nodes = {n.id: n for n in other.nodes()}
        left_edges = {e.id: e for e in self.graph.edges()}
        right_edges = {e.id: e for e in other.edges()}
        return GraphDiff(
            added_nodes=tuple(sorted(right_nodes.keys() - left_nodes.keys())),
            removed_nodes=tuple(sorted(left_nodes.keys() - right_nodes.keys())),
            changed_nodes=tuple(sorted(k for k in left_nodes.keys() & right_nodes.keys()
                                       if left_nodes[k] != right_nodes[k])),
            added_edges=tuple(sorted(right_edges.keys() - left_edges.keys())),
            removed_edges=tuple(sorted(left_edges.keys() - right_edges.keys())),
            changed_edges=tuple(sorted(k for k in left_edges.keys() & right_edges.keys()
                                       if left_edges[k] != right_edges[k])),
        )

    def snapshot(self) -> KnowledgeGraph:
        return self.graph.copy()
