from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Mapping

@dataclass(frozen=True)
class ClaimQualityRubric:
    """Weights for explicit, human- or model-assessed claim-quality dimensions."""
    weights: Mapping[str,float] = field(default_factory=lambda: {
        "clarity":0.20, "specificity":0.20, "falsifiability":0.15,
        "evidence_traceability":0.25, "scope":0.10, "temporal_precision":0.10})
    def __post_init__(self):
        if not self.weights: raise ValueError("rubric must contain dimensions")
        if any(v < 0 for v in self.weights.values()) or sum(self.weights.values()) <= 0:
            raise ValueError("rubric weights must be non-negative with positive total")

@dataclass(frozen=True)
class ClaimQualityScore:
    overall: float
    dimension_scores: dict[str,float]
    normalized_weights: dict[str,float]
    missing_dimensions: tuple[str,...]
    interpretation: str

def evaluate_claim_quality(scores: Mapping[str,float],
                           rubric: ClaimQualityRubric | None=None) -> ClaimQualityScore:
    rubric=rubric or ClaimQualityRubric()
    unknown=set(scores)-set(rubric.weights)
    if unknown: raise ValueError(f"unknown rubric dimensions: {sorted(unknown)}")
    if not scores: raise ValueError("at least one dimension score is required")
    values={}
    for k,v in scores.items():
        if not 0 <= float(v) <= 1: raise ValueError(f"{k} must be between 0 and 1")
        values[k]=float(v)
    # Missing dimensions are not silently scored as zero; weights are renormalized.
    active_total=sum(rubric.weights[k] for k in values)
    if active_total <= 0: raise ValueError("scored dimensions must have positive total weight")
    weights={k:rubric.weights[k]/active_total for k in values}
    overall=sum(values[k]*weights[k] for k in values)
    missing=tuple(k for k in rubric.weights if k not in values)
    label=("strong" if overall>=.8 else "moderate" if overall>=.6
           else "weak" if overall>=.4 else "poor")
    note=f"{label} assessed claim quality"
    if missing: note += f"; {len(missing)} rubric dimension(s) not assessed"
    return ClaimQualityScore(overall,values,weights,missing,note)
