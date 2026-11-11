from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from collections import defaultdict
from typing import Any, Callable, Protocol
from .ids import new_id

@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    aggregate_id: str
    payload: dict[str,Any]
    def __post_init__(self):
        if not self.event_type.strip() or not self.aggregate_id.strip():
            raise ValueError("event_type and aggregate_id are required")

@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    event: DomainEvent
    occurred_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str | None=None
    causation_id: str | None=None
    schema_version: str="1"
    def __post_init__(self):
        if not self.event_id: raise ValueError("event_id required")
        if self.occurred_at.tzinfo is None: raise ValueError("occurred_at must be timezone-aware")

class EventBus(Protocol):
    def publish(self,envelope: EventEnvelope) -> None: ...
    def subscribe(self,event_type: str,handler: Callable[[EventEnvelope],None]) -> Callable[[],None]: ...

class InMemoryEventBus:
    """Synchronous process-local event bus. Handler exceptions propagate to publisher."""
    def __init__(self):
        self._handlers=defaultdict(list)
        self._lock=RLock()

    def publish(self,envelope: EventEnvelope) -> None:
        with self._lock:
            handlers=tuple(self._handlers.get(envelope.event.event_type,())) + tuple(self._handlers.get("*",()))
        for handler in handlers: handler(envelope)

    def subscribe(self,event_type: str,handler: Callable[[EventEnvelope],None]) -> Callable[[],None]:
        if not event_type or not callable(handler): raise ValueError("event_type and callable handler required")
        with self._lock: self._handlers[event_type].append(handler)
        def unsubscribe():
            with self._lock:
                if handler in self._handlers.get(event_type,[]): self._handlers[event_type].remove(handler)
        return unsubscribe

def make_envelope(event: DomainEvent, *, correlation_id=None, causation_id=None) -> EventEnvelope:
    return EventEnvelope(new_id("evt"),event,correlation_id=correlation_id,causation_id=causation_id)
