import pytest
from intelligence import *

def test_claim_evidence_reasoning():
    c=Claim("c1","The claim",subject="x",predicate="has_value",object="yes")
    e=Evidence("e1","source",reliability=.9)
    a=EvidenceAssessment("e1","c1",EvidenceRelation.SUPPORTS,relevance=1)
    r=Reasoner().evaluate(c,[e],[a])
    assert r.suggested_status == ClaimStatus.SUPPORTED
    assert r.confidence.score == 1

def test_contradiction_detection_is_structured():
    a=Claim("a","A",subject="x",predicate="p",object="one")
    b=Claim("b","B",subject="x",predicate="p",object="two")
    assert len(detect_contradictions([a,b])) == 1

def test_balanced_evidence_is_inconclusive():
    c=Claim("c","Claim")
    es=[Evidence("s","support",reliability=.8),Evidence("r","refute",reliability=.8)]
    ass=[EvidenceAssessment("s","c",EvidenceRelation.SUPPORTS),
         EvidenceAssessment("r","c",EvidenceRelation.REFUTES)]
    result=Reasoner().evaluate(c,es,ass)
    assert result.confidence.score == .5
    assert result.suggested_status == ClaimStatus.INCONCLUSIVE

def test_synthesis_traceability():
    c=Claim("c","Claim")
    e=Evidence("e","Source")
    a=EvidenceAssessment("e","c",EvidenceRelation.SUPPORTS)
    s=synthesize([c],[e],[a])
    assert s.supporting_claim_ids == ("c",)
    assert s.evidence_ids == ("e",)

def test_validation():
    with pytest.raises(ValueError): Evidence("","")
    with pytest.raises(ValueError): EvidenceAssessment("e","c",EvidenceRelation.SUPPORTS,1.1)
