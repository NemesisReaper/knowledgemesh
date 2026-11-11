from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from collections.abc import Mapping

class UtilityDimension(str, Enum):
    RELEVANCE="relevance"
    ACTIONABILITY="actionability"
    NOVELTY="novelty"
    REUSABILITY="reusability"
    EVIDENCE_QUALITY="evidence_quality"
    FRESHNESS="freshness"

@dataclass(frozen=True)
class UtilityScore:
    overall: float
    dimension_scores: dict[str,float]
    weights: dict[str,float]
    rationale: str = ""

def evaluate_utility(scores: Mapping[str,float], *,
                     weights: Mapping[str,float] | None=None,
                     rationale: str="") -> UtilityScore:
    """Compute a weighted utility score from caller-assessed [0,1] dimensions.

    Missing dimensions are omitted; weights are normalized over supplied dimensions.
    """
    if not scores: raise ValueError("at least one dimension score is required")
    normalized={}
    for key,value in scores.items():
        name=key.value if isinstance(key,UtilityDimension) else str(key)
        if not 0 <= float(value) <= 1: raise ValueError(f"{name} must be between 0 and 1")
        normalized[name]=float(value)
    raw_weights={}
    for key in normalized:
        source=weights or {}
        raw_weights[key]=float(source.get(key,1.0))
        if raw_weights[key] < 0: raise ValueError("weights cannot be negative")
    total=sum(raw_weights.values())
    if total <= 0: raise ValueError("at least one supplied dimension must have positive weight")
    normalized_weights={k:v/total for k,v in raw_weights.items()}
    overall=sum(normalized[k]*normalized_weights[k] for k in normalized)
    return UtilityScore(overall,normalized,normalized_weights,rationale)
