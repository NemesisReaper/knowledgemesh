from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import defaultdict, deque
from typing import Iterable

class LineageRelation(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    SPLIT_FROM = "split_from"
    MERGED_FROM = "merged_from"
    SUPERSEDES = "supersedes"

@dataclass(frozen=True)
class LineageEvent:
    event_id: str
    knowledge_id: str
    relation: LineageRelation
    parents: tuple[str, ...] = ()
    actor: str = "unknown"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    content_fingerprint: str | None = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.event_id or not self.knowledge_id: raise ValueError("event_id and knowledge_id required")
        if self.timestamp.tzinfo is None: raise ValueError("timestamp must be timezone-aware")

class LineageGraph:
    """Append-only lineage event graph with cycle and missing-parent checks."""
    def __init__(self):
        self._events: dict[str, LineageEvent] = {}
        self._children: dict[str, set[str]] = defaultdict(set)

    def add(self, event: LineageEvent) -> None:
        if event.event_id in self._events: raise ValueError("duplicate event_id")
        missing = [p for p in event.parents if p not in self._events]
        if missing: raise ValueError(f"unknown parent event(s): {missing}")
        if event.event_id in event.parents: raise ValueError("self-cycle")
        self._events[event.event_id] = event
        for parent in event.parents: self._children[parent].add(event.event_id)

    def get(self, event_id: str) -> LineageEvent: return self._events[event_id]
    def ancestors(self, event_id: str) -> list[LineageEvent]:
        seen, queue, out = set(), deque(self._events[event_id].parents), []
        while queue:
            current = queue.popleft()
            if current in seen: continue
            seen.add(current); out.append(self._events[current])
            queue.extend(self._events[current].parents)
        return out
    def descendants(self, event_id: str) -> list[LineageEvent]:
        seen, queue, out = set(), deque(self._children[event_id]), []
        while queue:
            current = queue.popleft()
            if current in seen: continue
            seen.add(current); out.append(self._events[current])
            queue.extend(self._children[current])
        return out
    def events_for(self, knowledge_id: str) -> list[LineageEvent]:
        return sorted((e for e in self._events.values() if e.knowledge_id == knowledge_id),
                      key=lambda e: (e.timestamp, e.event_id))
    def validate(self) -> list[str]:
        issues = []
        for event in self._events.values():
            for parent in event.parents:
                if parent not in self._events: issues.append(f"{event.event_id}: missing parent {parent}")
        return issues
    def __len__(self): return len(self._events)
