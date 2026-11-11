"""Federation primitives for independently operated KnowMesh nodes."""
from .peers import Peer, PeerStatus, PeerRegistry
from .capabilities import Capability, CapabilitySet
from .discovery import DiscoveryQuery, DiscoveryResult, discover_peers
from .routing import Route, Router
from .synchronization import SyncItem, SyncPlan, SyncState, plan_sync, apply_sync_receipt
from .resilience import RetryPolicy, CircuitBreaker, CircuitState
__all__ = ["Peer","PeerStatus","PeerRegistry","Capability","CapabilitySet",
           "DiscoveryQuery","DiscoveryResult","discover_peers","Route","Router",
           "SyncItem","SyncPlan","SyncState","plan_sync","apply_sync_receipt",
           "RetryPolicy","CircuitBreaker","CircuitState"]
