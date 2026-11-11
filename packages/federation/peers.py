from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Iterable

class PeerStatus(str, Enum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    QUARANTINED = "quarantined"

@dataclass(frozen=True)
class Peer:
    peer_id: str
    base_url: str
    public_key: str = ""
    status: PeerStatus = PeerStatus.UNKNOWN
    capabilities: tuple[str, ...] = ()
    regions: tuple[str, ...] = ()
    last_seen: datetime | None = None
    latency_ms: float | None = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.peer_id.strip(): raise ValueError("peer_id is required")
        if not self.base_url.startswith(("https://", "http://")):
            raise ValueError("base_url must be an HTTP(S) URL")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        if self.last_seen is not None and self.last_seen.tzinfo is None:
            raise ValueError("last_seen must be timezone-aware")

class PeerRegistry:
    """Thread-safe local registry. It does not perform network discovery."""
    def __init__(self):
        self._peers: dict[str, Peer] = {}
        self._lock = RLock()

    def register(self, peer: Peer, *, replace_existing: bool = True) -> Peer:
        with self._lock:
            if peer.peer_id in self._peers and not replace_existing:
                raise ValueError(f"peer already registered: {peer.peer_id}")
            self._peers[peer.peer_id] = peer
            return peer

    def get(self, peer_id: str) -> Peer:
        with self._lock: return self._peers[peer_id]

    def update_status(self, peer_id: str, status: PeerStatus, *,
                      latency_ms: float | None = None,
                      seen_at: datetime | None = None) -> Peer:
        with self._lock:
            current = self._peers[peer_id]
            updated = replace(current, status=status,
                latency_ms=current.latency_ms if latency_ms is None else latency_ms,
                last_seen=seen_at or datetime.now(timezone.utc))
            self._peers[peer_id] = updated
            return updated

    def remove(self, peer_id: str) -> Peer:
        with self._lock: return self._peers.pop(peer_id)

    def list(self, *, statuses: Iterable[PeerStatus] | None = None) -> list[Peer]:
        with self._lock:
            peers = list(self._peers.values())
        if statuses is not None:
            allowed = set(statuses)
            peers = [p for p in peers if p.status in allowed]
        return sorted(peers, key=lambda p: p.peer_id)

    def __len__(self):
        with self._lock: return len(self._peers)
