"""Small instrumentation helpers for metrics and tracing."""

from __future__ import annotations

from functools import wraps
import time
from typing import Any, Callable

from .metrics import Counter, Histogram


def instrument_callable(function: Callable, *,
                        calls: Counter | None = None,
                        duration: Histogram | None = None,
                        operation: str | None = None):
    """Wrap a synchronous callable with call-count and duration metrics."""
    name = operation or function.__qualname__

    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        status = "success"
        try:
            return function(*args, **kwargs)
        except Exception:
            status = "error"
            raise
        finally:
            elapsed = time.perf_counter() - start
            if calls is not None:
                calls.inc(labels={"operation": name, "status": status}
                          if calls.label_names == ("operation", "status")
                          else _labels_for(calls, name, status))
            if duration is not None:
                duration.observe(elapsed, labels={"operation": name}
                                 if duration.label_names == ("operation",)
                                 else _labels_for(duration, name, status))
    return wrapper


def _labels_for(metric, name, status):
    if not metric.label_names:
        return None
    values = {"operation": name, "status": status}
    return {key: values[key] for key in metric.label_names if key in values}


def timed(histogram: Histogram, *, operation: str):
    def decorator(function):
        return instrument_callable(function, duration=histogram, operation=operation)
    return decorator


def observe_request(registry, *, method: str, route: str, status_code: int,
                    duration_seconds: float) -> None:
    """Record bounded-cardinality HTTP request metrics.

    Callers should pass a route template (e.g. /bundles/{bundle_id}), never
    an unbounded raw URL or query string.
    """
    counter = getattr(registry, "_knowmesh_http_requests", None)
    histogram = getattr(registry, "_knowmesh_http_duration", None)
    if counter is None:
        counter = registry.counter(
            "knowmesh_http_requests", "HTTP requests",
            ("method", "route", "status_code"),
        )
        setattr(registry, "_knowmesh_http_requests", counter)
    if histogram is None:
        histogram = registry.histogram(
            "knowmesh_http_request_duration_seconds", "HTTP request duration",
            ("method", "route"),
        )
        setattr(registry, "_knowmesh_http_duration", histogram)
    counter.inc(labels={"method": method.upper(), "route": route,
                        "status_code": str(status_code)})
    histogram.observe(duration_seconds, labels={"method": method.upper(), "route": route})
