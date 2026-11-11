from dataclasses import dataclass
from collections.abc import Iterable
from .evidence import Evidence, EvidenceAssessment, EvidenceRelation

@dataclass(frozen=True)
class ConfidenceAssessment:
    score: float
    support_weight: float
    refutation_weight: float
    evidence_count: int
    supporting_count: int
    refuting_count: int
    explanation: str

def assess_confidence(evidence: Iterable[Evidence],
                      assessments: Iterable[EvidenceAssessment]) -> ConfidenceAssessment:
    """Heuristic evidence balance, not a calibrated probability or truth score."""
    by_id = {e.evidence_id:e for e in evidence}
    support = refute = 0.0
    n_support = n_refute = 0
    used = set()
    for a in assessments:
        e = by_id.get(a.evidence_id)
        if e is None: continue
        weight = (e.reliability if e.reliability is not None else 0.5) * a.relevance
        if a.relation == EvidenceRelation.SUPPORTS:
            support += weight; n_support += 1; used.add(e.evidence_id)
        elif a.relation == EvidenceRelation.REFUTES:
            refute += weight; n_refute += 1; used.add(e.evidence_id)
    total = support + refute
    score = 0.5 if total == 0 else support / total
    if total == 0: note = "No supporting or refuting evidence was assessed."
    elif support == refute: note = "Supporting and refuting evidence are balanced."
    elif support > refute: note = "Assessed evidence leans supportive."
    else: note = "Assessed evidence leans refutational."
    return ConfidenceAssessment(score, support, refute, len(used), n_support, n_refute, note)
