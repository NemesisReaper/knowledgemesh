"""Experimental outcome evaluation against hypotheses and protocols."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .execution import ExecutionAttempt, ExecutionStatus
from .hypotheses import Hypothesis, HypothesisStatus
from .protocols import ExperimentProtocol


@dataclass(frozen=True, slots=True)
class ExperimentOutcome:
    experiment_id: str
    hypothesis_id: str
    verdict: HypothesisStatus
    completed_trials: int
    mean_metrics: Mapping[str, float]
    confidence: float
    reasons: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


def evaluate_outcome(
    hypothesis: Hypothesis,
    protocol: ExperimentProtocol,
    attempts: Iterable[ExecutionAttempt],
) -> ExperimentOutcome:
    """Aggregate completed ExecutionAttempts and determine hypothesis verdict."""
    completed = [
        a for a in attempts
        if a.status == ExecutionStatus.COMPLETED and isinstance(a.output, Mapping)
    ]
    n = len(completed)
    reasons: list[str] = []

    if n < protocol.minimum_trials:
        reasons.append(f"completed trials ({n}) below protocol minimum ({protocol.minimum_trials})")
        return ExperimentOutcome(
            experiment_id=protocol.protocol_id,
            hypothesis_id=hypothesis.hypothesis_id,
            verdict=HypothesisStatus.INCONCLUSIVE,
            completed_trials=n,
            mean_metrics={},
            confidence=0.0,
            reasons=tuple(reasons),
        )

    metric_sums: dict[str, float] = {}
    metric_counts: dict[str, int] = {}
    for attempt in completed:
        for k, v in (attempt.output or {}).items():
            if isinstance(v, (int, float)):
                metric_sums[k] = metric_sums.get(k, 0.0) + float(v)
                metric_counts[k] = metric_counts.get(k, 0) + 1

    mean_metrics = {k: metric_sums[k] / metric_counts[k] for k in sorted(metric_sums)}
    missing_metrics = [m for m in protocol.required_metrics if m not in mean_metrics]
    if missing_metrics:
        reasons.append(f"missing required protocol metrics: {missing_metrics}")
        return ExperimentOutcome(
            experiment_id=protocol.protocol_id,
            hypothesis_id=hypothesis.hypothesis_id,
            verdict=HypothesisStatus.INCONCLUSIVE,
            completed_trials=n,
            mean_metrics=mean_metrics,
            confidence=0.0,
            reasons=tuple(reasons),
        )

    if hypothesis.expected_metric and hypothesis.expected_threshold is not None:
        if hypothesis.expected_metric not in mean_metrics:
            return ExperimentOutcome(
                experiment_id=protocol.protocol_id,
                hypothesis_id=hypothesis.hypothesis_id,
                verdict=HypothesisStatus.INCONCLUSIVE,
                completed_trials=n,
                mean_metrics=mean_metrics,
                confidence=0.0,
                reasons=(f"expected metric {hypothesis.expected_metric!r} not present in output",),
            )
        passed = hypothesis.evaluate_value(mean_metrics[hypothesis.expected_metric])
        verdict = HypothesisStatus.SUPPORTED if passed else HypothesisStatus.REFUTED
    else:
        verdict = HypothesisStatus.SUPPORTED

    confidence = min(1.0, n / max(1, protocol.minimum_trials))
    return ExperimentOutcome(
        experiment_id=protocol.protocol_id,
        hypothesis_id=hypothesis.hypothesis_id,
        verdict=verdict,
        completed_trials=n,
        mean_metrics=mean_metrics,
        confidence=round(confidence, 4),
        reasons=tuple(reasons),
    )

