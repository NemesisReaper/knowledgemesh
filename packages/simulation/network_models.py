"""Small deterministic graph model for federated knowledge networks."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
import math
from typing import Any, Mapping


class NetworkModelError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class NetworkNode:
    id: str
    capacity: float = 1.0
    available: bool = True
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.id:
            raise NetworkModelError("node id is required")
        if not math.isfinite(self.capacity) or self.capacity < 0:
            raise NetworkModelError("node capacity must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class NetworkEdge:
    source: str
    target: str
    latency_ms: float = 0.0
    bandwidth_mbps: float = 100.0
    available: bool = True
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.source == self.target:
            raise NetworkModelError("self edges are not supported")
        if self.latency_ms < 0 or not math.isfinite(self.latency_ms):
            raise NetworkModelError("latency_ms must be finite and non-negative")
        if self.bandwidth_mbps < 0 or not math.isfinite(self.bandwidth_mbps):
            raise NetworkModelError("bandwidth_mbps must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class NetworkMetrics:
    node_count: int
    edge_count: int
    available_node_count: int
    available_edge_count: int
    density: float
    average_degree: float
    connected_components: int
    average_shortest_path_latency_ms: float | None


@dataclass(frozen=True, slots=True)
class NetworkSnapshot:
    nodes: tuple[NetworkNode, ...]
    edges: tuple[NetworkEdge, ...]
    metrics: NetworkMetrics
    adjacency: Mapping[str, tuple[str, ...]]


class NetworkModel:
    """Undirected network topology with latency-weighted shortest paths."""
    def __init__(self) -> None:
        self._nodes: dict[str, NetworkNode] = {}
        self._edges: dict[tuple[str, str], NetworkEdge] = {}

    def add_node(self, node: NetworkNode) -> None:
        self._nodes[node.id] = node

    def add_edge(self, edge: NetworkEdge) -> None:
        if edge.source not in self._nodes or edge.target not in self._nodes:
            raise NetworkModelError("both edge endpoints must exist")
        key = tuple(sorted((edge.source, edge.target)))
        self._edges[key] = edge

    def remove_node(self, node_id: str) -> bool:
        if node_id not in self._nodes:
            return False
        del self._nodes[node_id]
        for key in list(self._edges):
            if node_id in key:
                del self._edges[key]
        return True

    def set_node_availability(self, node_id: str, available: bool) -> None:
        if node_id not in self._nodes:
            raise NetworkModelError(f"unknown node: {node_id}")
        old = self._nodes[node_id]
        self._nodes[node_id] = NetworkNode(old.id, old.capacity, available, old.attributes)

    def set_edge_availability(self, source: str, target: str, available: bool) -> None:
        key = tuple(sorted((source, target)))
        if key not in self._edges:
            raise NetworkModelError(f"unknown edge: {source}-{target}")
        old = self._edges[key]
        self._edges[key] = NetworkEdge(old.source, old.target, old.latency_ms,
                                       old.bandwidth_mbps, available, old.attributes)

    def snapshot(self) -> NetworkSnapshot:
        nodes = tuple(self._nodes.values())
        edges = tuple(self._edges.values())
        active_nodes = {node.id for node in nodes if node.available}
        adjacency: dict[str, list[str]] = {node_id: [] for node_id in active_nodes}
        active_edges = []
        for edge in edges:
            if edge.available and edge.source in active_nodes and edge.target in active_nodes:
                adjacency[edge.source].append(edge.target)
                adjacency[edge.target].append(edge.source)
                active_edges.append(edge)
        components = _components(adjacency)
        n = len(active_nodes)
        degrees = [len(value) for value in adjacency.values()]
        density = (2 * len(active_edges) / (n * (n - 1))) if n > 1 else 0.0
        paths = []
        for source in sorted(active_nodes):
            distances = _dijkstra(source, adjacency, active_edges)
            paths.extend(value for target, value in distances.items() if target != source and math.isfinite(value))
        metrics = NetworkMetrics(
            node_count=len(nodes), edge_count=len(edges),
            available_node_count=n, available_edge_count=len(active_edges),
            density=density, average_degree=(sum(degrees) / n if n else 0.0),
            connected_components=components,
            average_shortest_path_latency_ms=(sum(paths) / len(paths) if paths else None),
        )
        return NetworkSnapshot(nodes, edges, metrics,
                               {key: tuple(sorted(value)) for key, value in adjacency.items()})


def _components(adjacency: Mapping[str, list[str]]) -> int:
    unseen = set(adjacency)
    count = 0
    while unseen:
        count += 1
        start = unseen.pop()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
    return count


def _dijkstra(source: str, adjacency: Mapping[str, list[str]],
              edges: list[NetworkEdge]) -> dict[str, float]:
    weights = {}
    for edge in edges:
        weights[(edge.source, edge.target)] = edge.latency_ms
        weights[(edge.target, edge.source)] = edge.latency_ms
    distances = {node: math.inf for node in adjacency}
    distances[source] = 0.0
    visited = set()
    while len(visited) < len(adjacency):
        current = min((node for node in adjacency if node not in visited),
                      key=lambda node: distances[node], default=None)
        if current is None or math.isinf(distances[current]):
            break
        visited.add(current)
        for neighbor in adjacency[current]:
            candidate = distances[current] + weights[(current, neighbor)]
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
    return distances
