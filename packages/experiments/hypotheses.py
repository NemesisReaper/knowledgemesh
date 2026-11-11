"""Experiment hypothesis definitions and status transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


class HypothesisStatus(str, Enum):
    PROPOSED = "proposed"
    TESTING = "testing"
    SUPPORTED = "supported"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    domain: str = "general"
    claim_ids: tuple[str, ...] = ()
    expected_metric: str = ""
    expected_threshold: float | None = None
    comparison: str = ">="
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.hypothesis_id or not self.hypothesis_id.strip():
            raise ValueError("hypothesis_id is required")
        if not self.statement or not self.statement.strip():
            raise ValueError("statement is required")
        if self.comparison not in {">=", ">", "<=", "<", "=="}:
            raise ValueError("comparison must be one of '>=', '>', '<=', '<', '=='")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
        object.__setattr__(self, "status", HypothesisStatus(self.status))

    def evaluate_value(self, observed: float) -> bool:
        if self.expected_threshold is None:
            raise ValueError("expected_threshold is not configured on this hypothesis")
        target = float(self.expected_threshold)
        val = float(observed)
        if self.comparison == ">=":
            return val >= target
        if self.comparison == ">":
            return val > target
        if self.comparison == "<=":
            return val <= target
        if self.comparison == "<":
            return val < target
        return abs(val - target) <= 1e-9

