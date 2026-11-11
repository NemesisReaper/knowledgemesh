"""Structured experimental protocols for testing hypotheses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ProtocolStep:
    step_id: str
    description: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.step_id or not self.step_id.strip():
            raise ValueError("step_id is required")
        if not self.action or not self.action.strip():
            raise ValueError("action is required")


@dataclass(frozen=True, slots=True)
class ExperimentProtocol:
    protocol_id: str
    hypothesis_id: str
    name: str
    steps: tuple[ProtocolStep, ...]
    independent_variables: Mapping[str, Any] = field(default_factory=dict)
    control_variables: Mapping[str, Any] = field(default_factory=dict)
    required_metrics: tuple[str, ...] = ()
    minimum_trials: int = 1

    def __post_init__(self) -> None:
        if not self.protocol_id or not self.hypothesis_id or not self.name:
            raise ValueError("protocol_id, hypothesis_id, and name are required")
        if not self.steps:
            raise ValueError("protocol requires at least one step")
        step_ids = [s.step_id for s in self.steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("protocol step_ids must be unique")
        if self.minimum_trials < 1:
            raise ValueError("minimum_trials must be >= 1")

