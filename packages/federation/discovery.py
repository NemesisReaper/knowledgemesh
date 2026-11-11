from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .peers import Peer, PeerRegistry, PeerStatus

@dataclass(frozen=True)
class DiscoveryQuery:
    required_capabilities: tuple[str, ...] = ()
    regions: tuple[str, ...] = ()
    statuses: tuple[PeerStatus, ...] = (PeerStatus.ACTIVE, PeerStatus.DEGRADED)
    exclude_peer_ids: tuple[str, ...] = ()
    max_latency_ms: float | None = None
    limit: int = 50

    def __post_init__(self):
        if self.limit < 1: raise ValueError("limit must be positive")
        if self.max_latency_ms is not None and self.max_latency_ms < 0:
            raise ValueError("max_latency_ms cannot be negative")

@dataclass(frozen=True)
class DiscoveryResult:
    peers: tuple[Peer, ...]
    examined: int
    rejected: int

def discover_peers(registry: PeerRegistry, query: DiscoveryQuery) -> DiscoveryResult:
    candidates = registry.list()
    selected = []
    for p in candidates:
        if p.peer_id in query.exclude_peer_ids: continue
        if p.status not in query.statuses: continue
        if not set(query.required_capabilities).issubset(p.capabilities): continue
        if query.regions and not set(query.regions).intersection(p.regions): continue
        if query.max_latency_ms is not None:
            if p.latency_ms is None or p.latency_ms > query.max_latency_ms: continue
        selected.append(p)
    selected.sort(key=lambda p: (
        p.latency_ms if p.latency_ms is not None else float("inf"), p.peer_id))
    selected = selected[:query.limit]
    return DiscoveryResult(tuple(selected), len(candidates), len(candidates)-len(selected))
