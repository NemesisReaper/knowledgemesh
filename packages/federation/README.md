# KnowMesh Federation

Federation primitives for independent KnowMesh nodes: peer registry, capability matching,
peer discovery, route ranking, manifest-based synchronization planning and resilience state.

## Original package modules retained
- `peers.py`: peer metadata and thread-safe local registry.
- `capabilities.py`: capability declarations and compatibility.
- `discovery.py`: filter peers by capability, status, region and latency.
- `routing.py`: rank eligible peers for a requested operation.
- `synchronization.py`: compare manifests and plan push/pull/no-op/conflict actions.
- `resilience.py`: retry schedule and circuit-breaker state machine.

## Quick start
```python
from federation import Peer, PeerRegistry, PeerStatus, DiscoveryQuery, discover_peers

registry = PeerRegistry()
registry.register(Peer("node-b", "https://node-b.example",
                       status=PeerStatus.ACTIVE,
                       capabilities=("knowledge.read", "knowledge.verify")))
result = discover_peers(registry, DiscoveryQuery(
    required_capabilities=("knowledge.verify",)))
```

## Boundaries
- This package is a federation control-plane foundation, not a complete network protocol.
- It does not make HTTP calls, authenticate peers, exchange keys, or transfer artifact bytes.
- Peer registration is local; discovery across the internet requires a transport/registry adapter.
- Sync planning compares fingerprints. Divergent existing versions are marked as conflicts;
  three-way merge requires common-base metadata and a separate merge policy.
- Circuit breaker and retry policy expose state/decisions; callers implement sleeps and I/O.
- Integrate peer authentication with KnowMesh Trust and all outbound calls with allowlists,
  TLS validation, timeouts, request signing, quotas and SSRF protections.
