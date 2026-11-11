# KnowMesh Intelligence

Evidence-grounded reasoning primitives for evaluating claims and producing traceable synthesis.

## Modules
- `claims.py`: atomic claim model and epistemic status vocabulary.
- `evidence.py`: evidence records and explicit support/refutation assessments.
- `confidence.py`: transparent weighted evidence balance heuristic.
- `contradictions.py`: structured triple conflict detection.
- `reasoning.py`: claim evaluation and recorded rule applications.
- `synthesis.py`: deterministic synthesis with traceable claim/evidence IDs.

## Quick start
```python
from intelligence import Claim, Evidence, EvidenceAssessment, EvidenceRelation, Reasoner

claim = Claim("c-1", "Water boils at 100 C at 1 atm",
              subject="water", predicate="boiling_point_at_1_atm", object="100 C")
evidence = Evidence("e-1", "Experimental measurement ...", reliability=0.9)
assessment = EvidenceAssessment("e-1", "c-1", EvidenceRelation.SUPPORTS, relevance=0.95)
result = Reasoner().evaluate(claim, [evidence], [assessment])
print(result.suggested_status, result.confidence.score)
```

## Boundaries
- Confidence is an evidence-balance heuristic, not a calibrated probability.
- Reliability values are supplied by callers; this package does not authenticate sources.
- Contradiction detection only compares explicit structured triples; it is not natural-language NLI.
- Inference rules are recorded, not formally proven or automatically executed.
- Synthesis is deterministic aggregation, not generative summarization.
- A supported/contested/rejected status is not an assertion of objective truth.
- This package does not replace KnowMesh trust, provenance, freshness or verification services.
