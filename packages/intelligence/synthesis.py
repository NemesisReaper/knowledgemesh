from dataclasses import dataclass
from collections.abc import Iterable
from .claims import Claim
from .evidence import Evidence, EvidenceAssessment, EvidenceRelation
from .contradictions import detect_contradictions, Contradiction

@dataclass(frozen=True)
class Synthesis:
    summary: str
    supporting_claim_ids: tuple[str,...]
    contested_claim_ids: tuple[str,...]
    evidence_ids: tuple[str,...]
    contradictions: tuple[Contradiction,...]
    open_questions: tuple[str,...]

def synthesize(claims: Iterable[Claim], evidence: Iterable[Evidence],
               assessments: Iterable[EvidenceAssessment]) -> Synthesis:
    """Create a deterministic, traceable synthesis from supplied records."""
    claims=tuple(claims); evidence=tuple(evidence); assessments=tuple(assessments)
    by_id={c.claim_id:c for c in claims}
    support=set(); refute=set(); evidence_ids=set()
    for a in assessments:
        if a.claim_id not in by_id: continue
        evidence_ids.add(a.evidence_id)
        if a.relation == EvidenceRelation.SUPPORTS: support.add(a.claim_id)
        if a.relation == EvidenceRelation.REFUTES: refute.add(a.claim_id)
    contested = support & refute
    supported = support - refute
    contradictions=tuple(detect_contradictions(claims))
    questions=[]
    for c in claims:
        if c.claim_id not in support | refute:
            questions.append(f"What evidence would resolve: {c.statement}")
    lines=[]
    if supported: lines.append(f"{len(supported)} claim(s) have supporting evidence without assessed refutation.")
    if contested: lines.append(f"{len(contested)} claim(s) have both supporting and refuting evidence.")
    if contradictions: lines.append(f"{len(contradictions)} explicit structured contradiction(s) were detected.")
    if not lines: lines.append("The supplied records do not establish a supported conclusion.")
    return Synthesis(" ".join(lines),tuple(sorted(supported)),tuple(sorted(contested)),
                     tuple(sorted(evidence_ids)),contradictions,tuple(questions))
