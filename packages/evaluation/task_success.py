from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Iterable
from math import isfinite

@dataclass(frozen=True)
class TaskOutcome:
    task_id: str
    success: bool
    duration_seconds: float | None = None
    required_steps: int | None = None
    completed_steps: int | None = None
    retries: int = 0
    error_category: str | None = None
    def __post_init__(self):
        if not self.task_id: raise ValueError("task_id required")
        if self.duration_seconds is not None and (not isfinite(self.duration_seconds) or self.duration_seconds<0):
            raise ValueError("duration_seconds must be finite and non-negative")
        if self.retries < 0: raise ValueError("retries cannot be negative")
        if self.required_steps is not None and self.required_steps < 0: raise ValueError("required_steps cannot be negative")
        if self.completed_steps is not None and self.completed_steps < 0: raise ValueError("completed_steps cannot be negative")

@dataclass(frozen=True)
class TaskSuccessMetrics:
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    success_rate: float
    mean_duration_seconds: float | None
    mean_retries: float
    step_completion_rate: float | None
    error_counts: dict[str,int]

def evaluate_task_success(outcomes: Iterable[TaskOutcome]) -> TaskSuccessMetrics:
    outcomes=tuple(outcomes)
    if len({o.task_id for o in outcomes}) != len(outcomes): raise ValueError("task_id values must be unique")
    total=len(outcomes)
    durations=[o.duration_seconds for o in outcomes if o.duration_seconds is not None]
    step_pairs=[(o.completed_steps,o.required_steps) for o in outcomes
                if o.completed_steps is not None and o.required_steps is not None and o.required_steps>0]
    errors={}
    for o in outcomes:
        if o.error_category: errors[o.error_category]=errors.get(o.error_category,0)+1
    success=sum(o.success for o in outcomes)
    return TaskSuccessMetrics(total,success,total-success,success/total if total else 0.0,
        sum(durations)/len(durations) if durations else None,
        sum(o.retries for o in outcomes)/total if total else 0.0,
        sum(c for c,r in step_pairs)/sum(r for c,r in step_pairs) if step_pairs else None,
        dict(sorted(errors.items())))
