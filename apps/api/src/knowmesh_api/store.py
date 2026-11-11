"""Compatibility memory store backed by or synchronized with KnowMeshService."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any
from uuid import uuid4


class _SyncedTableDict(dict):
    def __init__(self, parent: "MemoryStore") -> None:
        super().__init__()
        self._parent = parent

    def clear(self) -> None:
        super().clear()
        if self._parent._service is not None:
            self._parent._service.reset_for_testing()


class MemoryStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._service: Any = None
        self._tables: dict[str, dict[str, Any]] = _SyncedTableDict(self)

    def bind_service(self, service: Any) -> None:
        self._service = service

    def reset(self) -> None:
        with self._lock:
            self._tables.clear()

    def list(self, table: str, limit: int = 50, offset: int = 0, query: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            vals = list(self._tables.get(table, {}).values())
            if query:
                vals = [v for v in vals if query.casefold() in str(v).casefold()]
            return [dict(v) for v in vals[offset : offset + limit]]

    def get(self, table: str, key: str) -> dict[str, Any] | None:
        with self._lock:
            v = self._tables.get(table, {}).get(key)
            return dict(v) if v else None

    def put(self, table: str, data: dict[str, Any], key: str | None = None) -> dict[str, Any]:
        with self._lock:
            key = key or data.get("id") or str(uuid4())
            item = dict(data, id=key)
            item.setdefault("created_at", datetime.now(timezone.utc).isoformat())
            self._tables.setdefault(table, {})[key] = item
            return dict(item)

    def delete(self, table: str, key: str) -> bool:
        with self._lock:
            return self._tables.get(table, {}).pop(key, None) is not None


store = MemoryStore()
