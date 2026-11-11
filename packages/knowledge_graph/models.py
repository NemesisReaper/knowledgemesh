"""Core graph data structures and integrity checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping
import threading


class GraphError(ValueError):
    pass


class NodeType(str, Enum):
    CLAIM = "claim"
    CONCEPT = "concept"
    ENTITY = "entity"
    DOCUMENT = "document"
    AGENT = "agent"
    SOURCE = "source"
    EXPERIMENT = "experiment"
    CUSTOM = "custom"


class EdgeType(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    DERIVED_FROM = "derived_from"
    REFERENCES = "references"
    RELATED_TO = "related_to"
    INSTANCE_OF = "instance_of"
    PART_OF = "part_of"
    CAUSED_BY = "caused_by"
    SUPERSEDES = "supersedes"
    PUBLISHED_BY = "published_by"
    CUSTOM = "custom"


@dataclass(frozen=True, slots=True)
class GraphNode:
    id: str
    node_type: NodeType
    label: str
    properties: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise GraphError("node id is required")
        if not self.label or not self.label.strip():
            raise GraphError("node label is required")
        try:
            object.__setattr__(self, "node_type", NodeType(self.node_type))
        except ValueError:
            raise GraphError(f"unsupported node type: {self.node_type}")
        if not isinstance(self.properties, Mapping):
            raise GraphError("node properties must be a mapping")


@dataclass(frozen=True, slots=True)
class GraphEdge:
    id: str
    source: str
    target: str
    edge_type: EdgeType
    weight: float = 1.0
    properties: Mapping[str, Any] = field(default_factory=dict)
    directed: bool = True

    def __post_init__(self):
        if not self.id or not self.source or not self.target:
            raise GraphError("edge id, source and target are required")
        if self.source == self.target and self.edge_type != EdgeType.RELATED_TO:
            # Self loops can be useful for related-to but are usually modeling mistakes.
            raise GraphError("self edges are only allowed for related_to")
        if not isinstance(self.weight, (int, float)) or self.weight < 0:
            raise GraphError("edge weight must be a non-negative number")
        try:
            object.__setattr__(self, "edge_type", EdgeType(self.edge_type))
        except ValueError:
            raise GraphError(f"unsupported edge type: {self.edge_type}")
        if not isinstance(self.properties, Mapping):
            raise GraphError("edge properties must be a mapping")


class KnowledgeGraph:
    """Thread-safe in-memory directed/mixed multigraph.

    Parallel edges are allowed when they have distinct IDs. Node and edge
    objects are immutable dataclasses; their property mappings should be
    treated as immutable by callers.
    """
    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._out: dict[str, set[str]] = {}
        self._in: dict[str, set[str]] = {}
        self._lock = threading.RLock()
        self._generation = 0

    @property
    def generation(self) -> int:
        with self._lock:
            return self._generation

    def __len__(self) -> int:
        with self._lock:
            return len(self._nodes)

    def add_node(self, node: GraphNode, *, replace: bool = False) -> GraphNode:
        with self._lock:
            if node.id in self._nodes and not replace:
                if self._nodes[node.id] == node:
                    return node
                raise GraphError(f"node already exists: {node.id}")
            self._nodes[node.id] = node
            self._out.setdefault(node.id, set())
            self._in.setdefault(node.id, set())
            self._generation += 1
            return node

    def add_edge(self, edge: GraphEdge, *, replace: bool = False) -> GraphEdge:
        with self._lock:
            if edge.source not in self._nodes or edge.target not in self._nodes:
                raise GraphError("both edge endpoints must exist before adding an edge")
            if edge.id in self._edges and not replace:
                if self._edges[edge.id] == edge:
                    return edge
                raise GraphError(f"edge already exists: {edge.id}")
            if edge.id in self._edges:
                old = self._edges[edge.id]
                self._out[old.source].discard(old.id)
                self._in[old.target].discard(old.id)
            self._edges[edge.id] = edge
            self._out[edge.source].add(edge.id)
            self._in[edge.target].add(edge.id)
            if not edge.directed:
                self._out[edge.target].add(edge.id)
                self._in[edge.source].add(edge.id)
            self._generation += 1
            return edge

    def get_node(self, node_id: str) -> GraphNode | None:
        with self._lock:
            return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> GraphEdge | None:
        with self._lock:
            return self._edges.get(edge_id)

    def nodes(self, *, node_type: NodeType | str | None = None) -> tuple[GraphNode, ...]:
        with self._lock:
            values = tuple(self._nodes.values())
        if node_type is not None:
            expected = NodeType(node_type)
            values = tuple(node for node in values if node.node_type == expected)
        return values

    def edges(self, *, edge_type: EdgeType | str | None = None) -> tuple[GraphEdge, ...]:
        with self._lock:
            values = tuple(self._edges.values())
        if edge_type is not None:
            expected = EdgeType(edge_type)
            values = tuple(edge for edge in values if edge.edge_type == expected)
        return values

    def neighbors(self, node_id: str, *, direction: str = "out",
                  edge_types: Iterable[EdgeType | str] | None = None) -> tuple[tuple[GraphNode, GraphEdge], ...]:
        if direction not in {"out", "in", "both"}:
            raise GraphError("direction must be out, in or both")
        allowed = {EdgeType(item) for item in edge_types} if edge_types is not None else None
        with self._lock:
            if node_id not in self._nodes:
                raise GraphError(f"unknown node: {node_id}")
            edge_ids = set()
            if direction in {"out", "both"}:
                edge_ids.update(self._out[node_id])
            if direction in {"in", "both"}:
                edge_ids.update(self._in[node_id])
            result = []
            for edge_id in sorted(edge_ids):
                edge = self._edges[edge_id]
                if allowed is not None and edge.edge_type not in allowed:
                    continue
                if edge.source == node_id:
                    neighbor_id = edge.target
                elif edge.target == node_id:
                    neighbor_id = edge.source if not edge.directed or direction in {"in", "both"} else None
                else:
                    neighbor_id = None
                if neighbor_id is not None:
                    result.append((self._nodes[neighbor_id], edge))
            return tuple(result)

    def remove_edge(self, edge_id: str) -> bool:
        with self._lock:
            edge = self._edges.pop(edge_id, None)
            if edge is None:
                return False
            self._out[edge.source].discard(edge_id)
            self._in[edge.target].discard(edge_id)
            if not edge.directed:
                self._out[edge.target].discard(edge_id)
                self._in[edge.source].discard(edge_id)
            self._generation += 1
            return True

    def remove_node(self, node_id: str) -> bool:
        with self._lock:
            if node_id not in self._nodes:
                return False
            incident = set(self._out[node_id]) | set(self._in[node_id])
            for edge_id in incident:
                self.remove_edge(edge_id)
            del self._nodes[node_id]
            self._out.pop(node_id, None)
            self._in.pop(node_id, None)
            self._generation += 1
            return True

    def validate(self) -> tuple[str, ...]:
        errors = []
        with self._lock:
            for edge in self._edges.values():
                if edge.source not in self._nodes:
                    errors.append(f"edge {edge.id} has missing source {edge.source}")
                if edge.target not in self._nodes:
                    errors.append(f"edge {edge.id} has missing target {edge.target}")
            for node_id, edge_ids in self._out.items():
                for edge_id in edge_ids:
                    if edge_id not in self._edges:
                        errors.append(f"node {node_id} references missing outgoing edge {edge_id}")
        return tuple(errors)

    def copy(self) -> "KnowledgeGraph":
        clone = KnowledgeGraph()
        with self._lock:
            for node in self._nodes.values():
                clone.add_node(node)
            for edge in self._edges.values():
                clone.add_edge(edge)
        return clone
