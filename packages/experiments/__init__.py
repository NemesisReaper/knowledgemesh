"""Experiment hypotheses, protocols, execution attempts, outcomes, and reproducibility."""

from .execution import ExecutionAttempt, ExecutionStatus
from .hypotheses import Hypothesis, HypothesisStatus
from .outcomes import ExperimentOutcome, evaluate_outcome
from .protocols import ExperimentProtocol, ProtocolStep
from .reproducibility import (
    ReproducibilityAssessment,
    ReproducibilityManifest,
    assess_reproducibility,
)

__all__ = [
    "ExecutionAttempt",
    "ExecutionStatus",
    "Hypothesis",
    "HypothesisStatus",
    "ProtocolStep",
    "ExperimentProtocol",
    "ExperimentOutcome",
    "evaluate_outcome",
    "ReproducibilityManifest",
    "ReproducibilityAssessment",
    "assess_reproducibility",
]
