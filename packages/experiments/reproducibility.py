"""Reproducibility manifests and cross-run consistency checks for experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Iterable, Mapping

from .execution import ExecutionAttempt, ExecutionStatus


@dataclass(frozen=True, slots=True)
class ReproducibilityManifest:
    seed: int
    environment_fingerprint: str
    code_revision: str = "HEAD"
    dataset_digest: str = ""
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.environment_fingerprint or not self.environment_fingerprint.strip():
            raise ValueError("environment_fingerprint is required")

    def digest(self) -> str:
        payload = json.dumps(
            {
                "seed": self.seed,
                "environment_fingerprint": self.environment_fingerprint,
                "code_revision": self.code_revision,
                "dataset_digest": self.dataset_digest,
                "parameters": dict(self.parameters),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return "sha256:" + hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class ReproducibilityAssessment:
    reproducible: bool
    max_relative_deviation: float
    tolerance: float
    compared_runs: int
    reasons: tuple[str, ...] = ()


def assess_reproducibility(
    attempts: Iterable[ExecutionAttempt],
    *,
    metric: str,
    tolerance: float = 0.05,
) -> ReproducibilityAssessment:
    """Assess whether multiple completed runs reproduce a metric within relative tolerance."""
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    completed = [
        a for a in attempts
        if a.status == ExecutionStatus.COMPLETED
        and isinstance(a.output, Mapping)
        and isinstance(a.output.get(metric), (int, float))
    ]
    if len(completed) < 2:
        return ReproducibilityAssessment(
            reproducible=False,
            max_relative_deviation=0.0,
            tolerance=tolerance,
            compared_runs=len(completed),
            reasons=("at least two completed runs with the target metric are required",),
        )

    values = [float(a.output[metric]) for a in completed if a.output is not None]
    mean = sum(values) / len(values)
    denom = max(abs(mean), 1e-9)
    max_dev = max(abs(v - mean) / denom for v in values)
    ok = max_dev <= tolerance
    reasons = () if ok else (f"max relative deviation {max_dev:.4f} exceeds tolerance {tolerance:.4f}",)
    return ReproducibilityAssessment(
        reproducible=ok,
        max_relative_deviation=round(max_dev, 6),
        tolerance=tolerance,
        compared_runs=len(completed),
        reasons=reasons,
    )

