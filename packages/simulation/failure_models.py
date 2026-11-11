"""Explicit, reproducible failure injection models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Any, Mapping


class FailureType(str, Enum):
    NODE_UNAVAILABLE = "node_unavailable"
    HIGH_LATENCY = "high_latency"
    PACKET_LOSS = "packet_loss"
    DATA_CORRUPTION = "data_corruption"
    STALE_REPLICA = "stale_replica"
    AUTHENTICATION_FAILURE = "authentication_failure"
    RATE_LIMITED = "rate_limited"


class FailureSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class FailureModel:
    id: str
    failure_type: FailureType
    probability: float = 1.0
    severity: FailureSeverity = FailureSeverity.MEDIUM
    duration_seconds: float | None = None
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("failure model id is required")
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        if self.duration_seconds is not None and self.duration_seconds < 0:
            raise ValueError("duration_seconds cannot be negative")
        _validate_parameters(self.failure_type, self.parameters)


@dataclass(frozen=True, slots=True)
class FailureEvent:
    model_id: str
    failure_type: FailureType
    severity: FailureSeverity
    triggered: bool
    target_id: str | None
    effects: Mapping[str, Any]
    seed: int | None = None


def _validate_parameters(kind: FailureType, params: Mapping[str, Any]) -> None:
    if kind == FailureType.HIGH_LATENCY:
        delay = params.get("delay_ms", 1000)
        if not isinstance(delay, (int, float)) or delay < 0:
            raise ValueError("delay_ms must be a non-negative number")
    if kind == FailureType.PACKET_LOSS:
        rate = params.get("loss_rate", 0.1)
        if not isinstance(rate, (int, float)) or not 0 <= rate <= 1:
            raise ValueError("loss_rate must be between 0 and 1")
    if kind == FailureType.DATA_CORRUPTION:
        rate = params.get("corruption_rate", 1.0)
        if not isinstance(rate, (int, float)) or not 0 <= rate <= 1:
            raise ValueError("corruption_rate must be between 0 and 1")


def sample_failure(model: FailureModel, *, seed: int | None = None,
                   target_id: str | None = None) -> FailureEvent:
    """Sample whether a failure occurs; same seed gives same outcome."""
    rng = random.Random(seed)
    triggered = rng.random() < model.probability
    effects: dict[str, Any] = {}
    if triggered:
        if model.failure_type == FailureType.NODE_UNAVAILABLE:
            effects = {"available": False}
        elif model.failure_type == FailureType.HIGH_LATENCY:
            effects = {"additional_latency_ms": float(model.parameters.get("delay_ms", 1000))}
        elif model.failure_type == FailureType.PACKET_LOSS:
            effects = {"packet_loss_rate": float(model.parameters.get("loss_rate", 0.1))}
        elif model.failure_type == FailureType.DATA_CORRUPTION:
            effects = {"corruption_rate": float(model.parameters.get("corruption_rate", 1.0))}
        elif model.failure_type == FailureType.STALE_REPLICA:
            effects = {"stale": True, "lag_seconds": float(model.parameters.get("lag_seconds", 300))}
        elif model.failure_type == FailureType.AUTHENTICATION_FAILURE:
            effects = {"authentication_allowed": False}
        elif model.failure_type == FailureType.RATE_LIMITED:
            effects = {"rate_limited": True,
                       "retry_after_seconds": float(model.parameters.get("retry_after_seconds", 60))}
    return FailureEvent(model.id, model.failure_type, model.severity,
                        triggered, target_id, effects, seed)


def apply_failure(state: Mapping[str, Any], event: FailureEvent) -> dict[str, Any]:
    """Return a copied state with simulated effects; never mutates input."""
    result = dict(state)
    if not event.triggered:
        return result
    if event.failure_type == FailureType.NODE_UNAVAILABLE:
        result["available"] = False
    elif event.failure_type == FailureType.HIGH_LATENCY:
        result["latency_ms"] = float(result.get("latency_ms", 0)) + event.effects["additional_latency_ms"]
    elif event.failure_type == FailureType.PACKET_LOSS:
        result["packet_loss_rate"] = min(
            1.0, float(result.get("packet_loss_rate", 0)) + event.effects["packet_loss_rate"]
        )
    elif event.failure_type == FailureType.DATA_CORRUPTION:
        result["data_integrity"] = "potentially_corrupted"
        result["corruption_rate"] = event.effects["corruption_rate"]
    elif event.failure_type == FailureType.STALE_REPLICA:
        result["stale"] = True
        result["replication_lag_seconds"] = event.effects["lag_seconds"]
    elif event.failure_type == FailureType.AUTHENTICATION_FAILURE:
        result["authenticated"] = False
    elif event.failure_type == FailureType.RATE_LIMITED:
        result["rate_limited"] = True
        result["retry_after_seconds"] = event.effects["retry_after_seconds"]
    return result
