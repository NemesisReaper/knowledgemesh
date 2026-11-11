from __future__ import annotations
from dataclasses import dataclass
from .peers import Peer, PeerStatus

@dataclass(frozen=True)
class Route:
    peer: Peer
    score: float
    reasons: tuple[str, ...]

class Router:
    """Select a peer using capability fit, status and latency; never makes a request."""
    STATUS_WEIGHT = {PeerStatus.ACTIVE: 1.0, PeerStatus.DEGRADED: 0.55,
                     PeerStatus.UNKNOWN: 0.2, PeerStatus.UNAVAILABLE: 0.0,
                     PeerStatus.QUARANTINED: 0.0}

    def rank(self, peers: list[Peer], *, required_capabilities=(),
             preferred_regions=(), excluded_peer_ids=(), limit=10) -> list[Route]:
        if limit < 1: raise ValueError("limit must be positive")
        required=set(required_capabilities); regions=set(preferred_regions)
        routes=[]
        for peer in peers:
            if peer.peer_id in excluded_peer_ids: continue
            if not required.issubset(peer.capabilities): continue
            status_score=self.STATUS_WEIGHT[peer.status]
            if status_score == 0: continue
            latency_score = 1.0 if peer.latency_ms is None else 1.0/(1.0+peer.latency_ms/100.0)
            region_score = 1.0 if not regions or regions.intersection(peer.regions) else 0.65
            score = 0.55*status_score + 0.30*latency_score + 0.15*region_score
            reasons=(f"status={peer.status.value}", f"latency_ms={peer.latency_ms}",
                     "required capabilities satisfied",
                     "preferred region matched" if region_score == 1 else "region not preferred")
            routes.append(Route(peer,score,reasons))
        return sorted(routes,key=lambda r:(-r.score,r.peer.peer_id))[:limit]

    def select(self, peers: list[Peer], **kwargs) -> Route | None:
        ranked=self.rank(peers,limit=1,**kwargs)
        return ranked[0] if ranked else None
