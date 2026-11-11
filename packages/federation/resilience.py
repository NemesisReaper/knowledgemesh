from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta, timezone
from threading import RLock

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    initial_delay_seconds: float = 0.25
    multiplier: float = 2.0
    max_delay_seconds: float = 5.0
    jitter_ratio: float = 0.0

    def __post_init__(self):
        if self.max_attempts < 1: raise ValueError("max_attempts must be >= 1")
        if self.initial_delay_seconds < 0 or self.max_delay_seconds < 0:
            raise ValueError("delays cannot be negative")
        if self.multiplier < 1: raise ValueError("multiplier must be >= 1")
        if not 0 <= self.jitter_ratio <= 1: raise ValueError("jitter_ratio must be in [0,1]")

    def delay_for(self, failed_attempt: int) -> float:
        if failed_attempt < 1: raise ValueError("failed_attempt starts at 1")
        return min(self.max_delay_seconds,
                   self.initial_delay_seconds * self.multiplier ** (failed_attempt-1))

class CircuitState(str, Enum):
    CLOSED="closed"
    OPEN="open"
    HALF_OPEN="half_open"

class CircuitBreaker:
    """Thread-safe circuit breaker state machine; caller owns waiting and I/O."""
    def __init__(self, failure_threshold=5, reset_timeout_seconds=30.0):
        if failure_threshold < 1 or reset_timeout_seconds < 0:
            raise ValueError("invalid circuit breaker configuration")
        self.failure_threshold=failure_threshold
        self.reset_timeout=reset_timeout_seconds
        self._state=CircuitState.CLOSED
        self._failures=0
        self._opened_at=None
        self._lock=RLock()

    @property
    def state(self):
        with self._lock: return self._state

    def allow_request(self, now: datetime | None = None) -> bool:
        now=now or datetime.now(timezone.utc)
        if now.tzinfo is None: raise ValueError("now must be timezone-aware")
        with self._lock:
            if self._state == CircuitState.CLOSED: return True
            if self._state == CircuitState.OPEN:
                if self._opened_at is not None and (now-self._opened_at).total_seconds() >= self.reset_timeout:
                    self._state=CircuitState.HALF_OPEN
                    return True
                return False
            return False

    def record_success(self):
        with self._lock:
            self._failures=0; self._opened_at=None; self._state=CircuitState.CLOSED

    def record_failure(self, now: datetime | None = None):
        now=now or datetime.now(timezone.utc)
        with self._lock:
            self._failures += 1
            if self._state == CircuitState.HALF_OPEN or self._failures >= self.failure_threshold:
                self._state=CircuitState.OPEN; self._opened_at=now

    def reset(self):
        with self._lock:
            self._failures=0; self._opened_at=None; self._state=CircuitState.CLOSED
