"""Counterfactual experiments over isolated copies of network state."""

from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any, Callable, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class Intervention:
    """A named, declarative state change.

    Supported operations: set, add, multiply, remove. Dotted paths address
    nested dictionaries only; no Python expressions are evaluated.
    """
    path: str
    operation: str
    value: Any = None

    def __post_init__(self):
        if not self.path or any(not part for part in self.path.split(".")):
            raise ValueError("intervention path must be a non-empty dotted path")
        if self.operation not in {"set", "add", "multiply", "remove"}:
            raise ValueError("unsupported intervention operation")


@dataclass(frozen=True, slots=True)
class Counterfactual:
    id: str
    name: str
    interventions: tuple[Intervention, ...]
    description: str = ""

    def __post_init__(self):
        if not self.id or not self.name:
            raise ValueError("counterfactual id and name are required")


@dataclass(frozen=True, slots=True)
class CounterfactualResult:
    counterfactual_id: str
    baseline_state: Mapping[str, Any]
    intervention_state: Mapping[str, Any]
    baseline_outcome: Any
    intervention_outcome: Any
    delta: Any
    changed_paths: tuple[str, ...]


class CounterfactualSimulator:
    """Evaluate a baseline and intervention using a caller-provided model."""
    def __init__(self, evaluator: Callable[[Mapping[str, Any]], Any]) -> None:
        if not callable(evaluator):
            raise TypeError("evaluator must be callable")
        self.evaluator = evaluator

    def run(self, initial_state: Mapping[str, Any],
            counterfactual: Counterfactual) -> CounterfactualResult:
        baseline = deepcopy(dict(initial_state))
        altered = deepcopy(dict(initial_state))
        baseline_outcome = self.evaluator(deepcopy(baseline))
        changed = []
        for intervention in counterfactual.interventions:
            _apply(altered, intervention)
            changed.append(intervention.path)
        intervention_outcome = self.evaluator(deepcopy(altered))
        return CounterfactualResult(
            counterfactual_id=counterfactual.id,
            baseline_state=baseline,
            intervention_state=altered,
            baseline_outcome=baseline_outcome,
            intervention_outcome=intervention_outcome,
            delta=_delta(baseline_outcome, intervention_outcome),
            changed_paths=tuple(changed),
        )


def _apply(state: dict[str, Any], intervention: Intervention) -> None:
    parts = intervention.path.split(".")
    target = state
    for part in parts[:-1]:
        child = target.get(part)
        if not isinstance(child, dict):
            raise ValueError(f"path parent is not a dictionary: {part}")
        target = child
    key = parts[-1]
    if intervention.operation == "remove":
        if key not in target:
            raise KeyError(intervention.path)
        del target[key]
    elif intervention.operation == "set":
        target[key] = deepcopy(intervention.value)
    else:
        if key not in target or not isinstance(target[key], (int, float)):
            raise ValueError(f"{intervention.operation} requires numeric target: {intervention.path}")
        if not isinstance(intervention.value, (int, float)):
            raise ValueError("numeric intervention value required")
        if intervention.operation == "add":
            target[key] += intervention.value
        else:
            target[key] *= intervention.value


def _delta(before: Any, after: Any) -> Any:
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return after - before
    if isinstance(before, Mapping) and isinstance(after, Mapping):
        keys = set(before) | set(after)
        return {key: _delta(before.get(key), after.get(key))
                for key in sorted(keys) if before.get(key) != after.get(key)}
    return {"before": before, "after": after}


def compare_outcomes(baseline: Any, alternative: Any) -> Any:
    """Public helper for computing a simple outcome delta."""
    return _delta(baseline, alternative)
