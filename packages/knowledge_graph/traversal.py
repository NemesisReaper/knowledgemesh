"""Graph traversal algorithms with explicit direction and edge filtering."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from typing import Iterable

from .models import EdgeType, GraphEdge, GraphNode, KnowledgeGraph


@dataclass(frozen=True, slots=True)
class TraversalStep:
    node: GraphNode
    depth: int
    via_edge: GraphEdge | None = None


@dataclass(frozen=True, slots=True)
class TraversalResult:
    steps: tuple[TraversalStep, ...]
    truncated: bool = False

    @property
    def nodes(self) -> tuple[GraphNode, ...]:
        return tuple(step.node for step in self.steps)


def _validate(graph: KnowledgeGraph, start_id: str, direction: str,
              edge_types: Iterable[EdgeType | str] | None):
    if graph.get_node(start_id) is None:
        raise ValueError(f"unknown start node: {start_id}")
    if direction not in {"out", "in", "both"}:
        raise ValueError("direction must be out, in or both")
    return {EdgeType(t) for t in edge_types} if edge_types is not None else None


def breadth_first(graph: KnowledgeGraph, start_id: str, *,
                  direction: str = "out",
                  edge_types: Iterable[EdgeType | str] | None = None,
                  max_depth: int | None = None, limit: int = 1000) -> TraversalResult:
    allowed = _validate(graph, start_id, direction, edge_types)
    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth cannot be negative")
    if limit < 1:
        raise ValueError("limit must be >= 1")
    queue = deque([(start_id, 0, None)])
    visited = {start_id}
    steps = []
    truncated = False
    while queue:
        node_id, depth, via = queue.popleft()
        if len(steps) >= limit:
            truncated = True
            break
        steps.append(TraversalStep(graph.get_node(node_id), depth, via))
        if max_depth is not None and depth >= max_depth:
            continue
        for neighbor, edge in graph.neighbors(node_id, direction=direction, edge_types=allowed):
            if neighbor.id not in visited:
                visited.add(neighbor.id)
                queue.append((neighbor.id, depth + 1, edge))
    return TraversalResult(tuple(steps), truncated)


def depth_first(graph: KnowledgeGraph, start_id: str, *,
                direction: str = "out",
                edge_types: Iterable[EdgeType | str] | None = None,
                max_depth: int | None = None, limit: int = 1000) -> TraversalResult:
    allowed = _validate(graph, start_id, direction, edge_types)
    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth cannot be negative")
    if limit < 1:
        raise ValueError("limit must be >= 1")
    stack = [(start_id, 0, None)]
    visited = set()
    steps = []
    truncated = False
    while stack:
        node_id, depth, via = stack.pop()
        if node_id in visited:
            continue
        if len(steps) >= limit:
            truncated = True
            break
        visited.add(node_id)
        steps.append(TraversalStep(graph.get_node(node_id), depth, via))
        if max_depth is not None and depth >= max_depth:
            continue
        neighbors = graph.neighbors(node_id, direction=direction, edge_types=allowed)
        for neighbor, edge in reversed(neighbors):
            if neighbor.id not in visited:
                stack.append((neighbor.id, depth + 1, edge))
    return TraversalResult(tuple(steps), truncated)


def shortest_path(graph: KnowledgeGraph, source: str, target: str, *,
                  direction: str = "out",
                  edge_types: Iterable[EdgeType | str] | None = None) -> tuple[GraphNode, ...] | None:
    allowed = _validate(graph, source, direction, edge_types)
    if graph.get_node(target) is None:
        raise ValueError(f"unknown target node: {target}")
    distances = {source: 0.0}
    previous = {}
    heap = [(0.0, source)]
    while heap:
        distance, node_id = heapq.heappop(heap)
        if distance != distances.get(node_id):
            continue
        if node_id == target:
            break
        for neighbor, edge in graph.neighbors(node_id, direction=direction, edge_types=allowed):
            candidate = distance + float(edge.weight)
            if candidate < distances.get(neighbor.id, float("inf")):
                distances[neighbor.id] = candidate
                previous[neighbor.id] = node_id
                heapq.heappush(heap, (candidate, neighbor.id))
    if target not in distances:
        return None
    path = [target]
    while path[-1] != source:
        path.append(previous[path[-1]])
    path.reverse()
    return tuple(graph.get_node(node_id) for node_id in path)


def all_paths(graph: KnowledgeGraph, source: str, target: str, *,
              direction: str = "out",
              edge_types: Iterable[EdgeType | str] | None = None,
              max_depth: int = 5, limit: int = 100) -> tuple[tuple[GraphNode, ...], ...]:
    allowed = _validate(graph, source, direction, edge_types)
    if graph.get_node(target) is None:
        raise ValueError(f"unknown target node: {target}")
    if max_depth < 0 or limit < 1:
        raise ValueError("max_depth must be >= 0 and limit >= 1")
    results = []
    stack = [(source, (source,))]
    while stack and len(results) < limit:
        current, path = stack.pop()
        if current == target:
            results.append(tuple(graph.get_node(node_id) for node_id in path))
            continue
        if len(path) - 1 >= max_depth:
            continue
        neighbors = graph.neighbors(current, direction=direction, edge_types=allowed)
        for neighbor, _edge in reversed(neighbors):
            if neighbor.id not in path:
                stack.append((neighbor.id, path + (neighbor.id,)))
    return tuple(results)
