from dataclasses import dataclass, field
from collections.abc import Iterable, Mapping
from .claims import Claim, ClaimStatus
from .evidence import Evidence, EvidenceAssessment
from .confidence import assess_confidence, ConfidenceAssessment
from .contradictions import detect_contradictions, Contradiction

@dataclass(frozen=True)
class Inference:
    inference_id: str
    conclusion: str
    premise_claim_ids: tuple[str,...]
    rule: str
    rationale: str = ""

@dataclass(frozen=True)
class ReasoningResult:
    claim_id: str
    confidence: ConfidenceAssessment
    contradictions: tuple[Contradiction,...]
    suggested_status: ClaimStatus
    limitations: tuple[str,...] = ()

class Reasoner:
    """Transparent evidence aggregation and contradiction checks; no LLM dependency."""
    def evaluate(self, claim: Claim, evidence: Iterable[Evidence],
                 assessments: Iterable[EvidenceAssessment],
                 related_claims: Iterable[Claim] = ()) -> ReasoningResult:
        evidence = tuple(evidence); assessments = tuple(assessments)
        confidence = assess_confidence(evidence, assessments)
        contradictions = tuple(detect_contradictions((claim,*tuple(related_claims))))
        if contradictions:
            status = ClaimStatus.CONTESTED
        elif confidence.evidence_count == 0:
            status = ClaimStatus.INCONCLUSIVE
        elif confidence.score >= 0.75 and confidence.refutation_weight == 0:
            status = ClaimStatus.SUPPORTED
        elif confidence.score <= 0.25 and confidence.support_weight == 0:
            status = ClaimStatus.REJECTED
        else:
            status = ClaimStatus.INCONCLUSIVE
        return ReasoningResult(claim.claim_id,confidence,contradictions,status,
            ("Thresholds are heuristic and must be configured for the domain.",
             "Evidence authenticity, independence, freshness and selection bias require separate checks.",
             "A supported status is not a guarantee that the claim is true."))

    def apply_rule(self, rule_name: str, premises: Iterable[Claim],
                   conclusion: str, inference_id: str) -> Inference:
        premises = tuple(premises)
        if not premises: raise ValueError("at least one premise is required")
        return Inference(inference_id,conclusion,tuple(p.claim_id for p in premises),
                         rule_name,"Rule application is recorded; validity is not independently proven.")
