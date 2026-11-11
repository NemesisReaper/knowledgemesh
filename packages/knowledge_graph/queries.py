"""Declarative graph filtering and neighborhood queries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .models import EdgeType, GraphEdge, GraphNode, KnowledgeGraph, NodeType


@dataclass(frozen=True, slots=True)
class GraphQuery:
    node_types: tuple[NodeType | str, ...] = ()
    edge_types: tuple[EdgeType | str, ...] = ()
    properties: Mapping[str, Any] = field(default_factory=dict)
    label_contains: str | None = None
    start_ids: tuple[str, ...] = ()
    direction: str = "both"
    max_depth: int = 1
    limit: int = 100

    def __post_init__(self):
        if self.direction not in {"out", "in", "both"}:
            raise ValueError("direction must be out, in or both")
        if self.max_depth < 0:
            raise ValueError("max_depth cannot be negative")
        if self.limit < 1:
            raise ValueError("limit must be >= 1")


@dataclass(frozen=True, slots=True)
class QueryResult:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    truncated: bool = False


class QueryEngine:
    def __init__(self, graph: KnowledgeGraph) -> None:
        self.graph = graph

    def execute(self, query: GraphQuery) -> QueryResult:
        allowed_nodes = {NodeType(t) for t in query.node_types} if query.node_types else None
        allowed_edges = {EdgeType(t) for t in query.edge_types} if query.edge_types else None
        if query.start_ids:
            selected = self._reachable(query)
        else:
            selected = {node.id for node in self.graph.nodes()}
        matched = []
        for node_id in sorted(selected):
            node = self.graph.get_node(node_id)
            if node is None:
                continue
            if allowed_nodes is not None and node.node_type not in allowed_nodes:
                continue
            if query.label_contains and query.label_contains.casefold() not in node.label.casefold():
                continue
            if any(node.properties.get(key) != value for key, value in query.properties.items()):
                continue
            matched.append(node)
        truncated = len(matched) > query.limit
        matched = matched[:query.limit]
        ids = {node.id for node in matched}
        edges = tuple(edge for edge in self.graph.edges()
                      if edge.source in ids and edge.target in ids
                      and (allowed_edges is None or edge.edge_type in allowed_edges))
        return QueryResult(tuple(matched), edges, truncated)

    def _reachable(self, query: GraphQuery) -> set[str]:
        visited = set()
        frontier = set(query.start_ids)
        for start in frontier:
            if self.graph.get_node(start) is None:
                raise ValueError(f"unknown start node: {start}")
        for _ in range(query.max_depth + 1):
            new_frontier = set()
            for node_id in frontier:
                if node_id in visited:
                    continue
                visited.add(node_id)
                if len(visited) >= query.limit:
                    return visited
                for neighbor, _edge in self.graph.neighbors(
                    node_id, direction=query.direction,
                    edge_types=query.edge_types or None,
                ):
                    if neighbor.id not in visited:
                        new_frontier.add(neighbor.id)
            frontier = new_frontier
        return visited


def query_graph(graph: KnowledgeGraph, query: GraphQuery) -> QueryResult:
    return QueryEngine(graph).execute(query)
