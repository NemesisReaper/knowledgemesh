# KnowMesh Core

Shared, dependency-light primitives used across KnowMesh packages.

## Modules
- `ids.py`: prefixed UUID identifiers and ID validation.
- `errors.py`: consistent typed domain/service exceptions.
- `config.py`: validated environment-backed core settings.
- `serialization.py`: deterministic JSON-compatible conversion and content hashing.
- `events.py`: domain event envelope and process-local event bus protocol/implementation.
- `pagination.py`: bounded offset pagination primitives.
- `result.py`: explicit success/failure result type.

## Quick start
```python
from core import DomainEvent, EventEnvelope, InMemoryEventBus, new_id, stable_hash

bus = InMemoryEventBus()
received = []
bus.subscribe("knowledge.published", received.append)
event = DomainEvent("knowledge.published", "claim-42", {"version": 3})
bus.publish(EventEnvelope(new_id("evt"), event))
print(stable_hash({"claim_id": "claim-42", "version": 3}))
```

## Integration boundaries
- The original repository scaffold did not contain a `packages/core/` directory.
  This is a newly introduced shared foundation, not an implementation of existing core files.
- The event bus is synchronous and in-process; it is not durable and does not provide retries,
  ordering across processes, transactional outbox semantics, or delivery guarantees.
- `stable_hash` uses deterministic project-local JSON encoding, not RFC 8785/JCS.
- Configuration covers shared runtime defaults only; service-specific settings belong to services.
- IDs are identifiers, not authentication credentials or proof of ownership.
