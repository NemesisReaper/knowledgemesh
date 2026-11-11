"""Minimal W3C trace-context compatible tracing primitives."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from datetime import datetime, timezone
import secrets
import threading
import time
from typing import Any, Mapping, Protocol


class TraceExporter(Protocol):
    def export(self, span: "Span") -> None: ...


@dataclass(frozen=True, slots=True)
class SpanContext:
    trace_id: str
    span_id: str
    trace_flags: str = "01"

    def __post_init__(self):
        if len(self.trace_id) != 32 or len(self.span_id) != 16:
            raise ValueError("trace_id must be 32 hex chars and span_id 16")
        int(self.trace_id, 16)
        int(self.span_id, 16)
        if self.trace_id == "0" * 32 or self.span_id == "0" * 16:
            raise ValueError("trace and span IDs cannot be all zeroes")
        if len(self.trace_flags) != 2:
            raise ValueError("trace_flags must be two hex chars")
        int(self.trace_flags, 16)


@dataclass(frozen=True, slots=True)
class Span:
    name: str
    context: SpanContext
    parent_span_id: str | None
    started_at: datetime
    ended_at: datetime
    duration_seconds: float
    attributes: Mapping[str, Any] = field(default_factory=dict)
    status: str = "ok"
    error: str | None = None


_current_span: ContextVar[SpanContext | None] = ContextVar("knowmesh_current_span", default=None)


def current_span() -> SpanContext | None:
    return _current_span.get()


def trace_context() -> SpanContext | None:
    return current_span()


def traceparent_from_context(context: SpanContext | None = None) -> str | None:
    context = context or current_span()
    if context is None:
        return None
    return f"00-{context.trace_id}-{context.span_id}-{context.trace_flags}"


def parse_traceparent(value: str) -> SpanContext:
    parts = value.strip().split("-")
    if len(parts) != 4 or parts[0] != "00":
        raise ValueError("unsupported or malformed traceparent")
    return SpanContext(parts[1].lower(), parts[2].lower(), parts[3].lower())


class InMemoryTraceExporter:
    def __init__(self) -> None:
        self._spans: list[Span] = []
        self._lock = threading.Lock()

    def export(self, span: Span) -> None:
        with self._lock:
            self._spans.append(span)

    def spans(self) -> tuple[Span, ...]:
        with self._lock:
            return tuple(self._spans)


class Tracer:
    def __init__(self, service_name: str, exporter: TraceExporter | None = None) -> None:
        if not service_name:
            raise ValueError("service_name is required")
        self.service_name = service_name
        self.exporter = exporter

    @contextmanager
    def start_as_current_span(self, name: str, *,
                              attributes: Mapping[str, Any] | None = None,
                              parent: SpanContext | None = None):
        if not name:
            raise ValueError("span name is required")
        active_parent = parent or current_span()
        context = SpanContext(
            active_parent.trace_id if active_parent else secrets.token_hex(16),
            secrets.token_hex(8),
            active_parent.trace_flags if active_parent else "01",
        )
        token: Token = _current_span.set(context)
        started = datetime.now(timezone.utc)
        clock = time.perf_counter()
        status, error = "ok", None
        try:
            yield context
        except Exception as exc:
            status, error = "error", f"{type(exc).__name__}: {exc}"
            raise
        finally:
            span = Span(
                name=name, context=context,
                parent_span_id=active_parent.span_id if active_parent else None,
                started_at=started, ended_at=datetime.now(timezone.utc),
                duration_seconds=max(0.0, time.perf_counter() - clock),
                attributes={"service.name": self.service_name, **dict(attributes or {})},
                status=status, error=error,
            )
            _current_span.reset(token)
            if self.exporter is not None:
                self.exporter.export(span)
