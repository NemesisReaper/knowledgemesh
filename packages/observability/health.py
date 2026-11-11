"""Liveness/readiness health checks with bounded synchronous execution."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import threading
import time
from typing import Any, Callable, Mapping


class CheckError(ValueError):
    pass


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True, slots=True)
class HealthCheck:
    name: str
    check: Callable[[], Any]
    critical: bool = True
    timeout_seconds: float = 2.0

    def __post_init__(self):
        if not self.name or not callable(self.check):
            raise CheckError("health check requires name and callable")
        if self.timeout_seconds <= 0:
            raise CheckError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class HealthCheckResult:
    name: str
    status: HealthStatus
    duration_seconds: float
    critical: bool
    message: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class HealthReport:
    status: HealthStatus
    checked_at: datetime
    checks: tuple[HealthCheckResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "checked_at": self.checked_at.isoformat(),
            "checks": [{
                "name": c.name, "status": c.status.value,
                "duration_seconds": c.duration_seconds,
                "critical": c.critical, "message": c.message,
                "details": dict(c.details),
            } for c in self.checks],
        }


class HealthRegistry:
    def __init__(self, checks=()) -> None:
        self._checks: dict[str, HealthCheck] = {}
        self._lock = threading.RLock()
        for check in checks:
            self.register(check)

    def register(self, check: HealthCheck) -> None:
        with self._lock:
            if check.name in self._checks:
                raise CheckError(f"duplicate health check: {check.name}")
            self._checks[check.name] = check

    def run(self, *, names=None) -> HealthReport:
        with self._lock:
            selected = [self._checks[name] for name in names] if names is not None else list(self._checks.values())
        results = tuple(_run_check(check) for check in selected)
        if any(r.status == HealthStatus.UNHEALTHY and r.critical for r in results):
            overall = HealthStatus.UNHEALTHY
        elif any(r.status != HealthStatus.HEALTHY for r in results):
            overall = HealthStatus.DEGRADED
        else:
            overall = HealthStatus.HEALTHY
        return HealthReport(overall, datetime.now(timezone.utc), results)

    evaluate = run


def _run_check(check: HealthCheck) -> HealthCheckResult:
    start = time.perf_counter()
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(check.check)
    try:
        value = future.result(timeout=check.timeout_seconds)
        if isinstance(value, Mapping):
            ok = bool(value.get("ok", True))
            message = str(value.get("message", ""))
            details = {k: v for k, v in value.items() if k not in {"ok", "message"}}
        else:
            ok, message, details = value is not False, "", {}
        status = HealthStatus.HEALTHY if ok else HealthStatus.UNHEALTHY
    except FutureTimeout:
        future.cancel()
        status, message, details = HealthStatus.UNHEALTHY, "health check timed out", {}
    except Exception as exc:
        status, message, details = HealthStatus.UNHEALTHY, f"{type(exc).__name__}: {exc}", {}
    finally:
        # Do not wait for a timed-out check to finish.
        executor.shutdown(wait=False, cancel_futures=True)
    return HealthCheckResult(check.name, status, max(0.0, time.perf_counter() - start),
                             check.critical, message, details)
