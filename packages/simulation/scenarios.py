"""Deterministic scenario definitions and execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import time
from typing import Any, Callable, Mapping, Sequence


class ScenarioError(ValueError):
    """Invalid scenario definition or execution request."""


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class ScenarioStep:
    id: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    depends_on: tuple[str, ...] = ()
    optional: bool = False

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ScenarioError("step id cannot be empty")
        if not self.action or not self.action.strip():
            raise ScenarioError(f"step {self.id}: action cannot be empty")
        if self.id in self.depends_on:
            raise ScenarioError(f"step {self.id} cannot depend on itself")


@dataclass(frozen=True, slots=True)
class Scenario:
    id: str
    name: str
    steps: tuple[ScenarioStep, ...]
    description: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.name:
            raise ScenarioError("scenario id and name are required")
        ids = [step.id for step in self.steps]
        if len(ids) != len(set(ids)):
            raise ScenarioError("scenario step ids must be unique")
        known = set(ids)
        for step in self.steps:
            unknown = set(step.depends_on) - known
            if unknown:
                raise ScenarioError(
                    f"step {step.id} has unknown dependencies: {sorted(unknown)}"
                )
        _topological_order(self.steps)


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    scenario_id: str
    status: str
    step_results: Mapping[str, Mapping[str, Any]]
    started_at: datetime
    finished_at: datetime
    duration_seconds: float
    outputs: Mapping[str, Any] = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return self.status == "succeeded"


def _topological_order(steps: Sequence[ScenarioStep]) -> list[ScenarioStep]:
    by_id = {step.id: step for step in steps}
    remaining = set(by_id)
    completed: set[str] = set()
    ordered: list[ScenarioStep] = []
    while remaining:
        ready = sorted(
            (step_id for step_id in remaining
             if set(by_id[step_id].depends_on) <= completed)
        )
        if not ready:
            raise ScenarioError("scenario dependencies contain a cycle")
        for step_id in ready:
            ordered.append(by_id[step_id])
            completed.add(step_id)
            remaining.remove(step_id)
    return ordered


class ScenarioRunner:
    """Runs registered synchronous actions in dependency order.

    Actions receive a copy of step parameters and a read-only-by-convention
    mapping of completed step outputs. This runner is a local simulator; it
    does not execute arbitrary code from scenario documents.
    """
    def __init__(self, actions: Mapping[str, Callable[..., Any]] | None = None) -> None:
        self._actions = dict(actions or {})

    def register(self, name: str, action: Callable[..., Any]) -> None:
        if not name or not callable(action):
            raise ScenarioError("action name and callable are required")
        self._actions[name] = action

    def run(self, scenario: Scenario, *, stop_on_error: bool = True) -> ScenarioResult:
        started = datetime.now(timezone.utc)
        clock = time.monotonic()
        results: dict[str, dict[str, Any]] = {}
        outputs: dict[str, Any] = {}
        failed = False
        for step in _topological_order(scenario.steps):
            blocked = any(results.get(dep, {}).get("status") != StepStatus.SUCCEEDED.value
                          for dep in step.depends_on)
            if blocked or (failed and stop_on_error):
                results[step.id] = {"status": StepStatus.SKIPPED.value,
                                    "reason": "dependency failed or execution stopped"}
                continue
            action = self._actions.get(step.action)
            if action is None:
                error = f"action not registered: {step.action}"
                results[step.id] = {"status": StepStatus.FAILED.value, "error": error}
                failed = True
                if stop_on_error and not step.optional:
                    continue
                continue
            try:
                value = action(dict(step.parameters), dict(outputs))
                outputs[step.id] = value
                results[step.id] = {"status": StepStatus.SUCCEEDED.value,
                                    "output": value}
            except Exception as exc:
                results[step.id] = {
                    "status": StepStatus.FAILED.value,
                    "error": f"{type(exc).__name__}: {exc}",
                }
                failed = True
                if stop_on_error and not step.optional:
                    # Remaining steps are marked skipped by the dependency/stop rule.
                    continue
        status = "failed" if failed else "succeeded"
        finished = datetime.now(timezone.utc)
        return ScenarioResult(
            scenario_id=scenario.id, status=status, step_results=results,
            started_at=started, finished_at=finished,
            duration_seconds=max(0.0, time.monotonic() - clock),
            outputs=outputs,
        )
