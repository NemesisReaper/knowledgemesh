"""Evidence-grounded intelligence primitives for KnowMesh."""
from .claims import Claim, ClaimStatus
from .evidence import Evidence, EvidenceRelation, EvidenceAssessment
from .reasoning import Reasoner, ReasoningResult, Inference
from .contradictions import Contradiction, detect_contradictions
from .synthesis import Synthesis, synthesize
from .confidence import ConfidenceAssessment, assess_confidence
__all__ = ["Claim","ClaimStatus","Evidence","EvidenceRelation","EvidenceAssessment",
           "Reasoner","ReasoningResult","Inference","Contradiction","detect_contradictions",
           "Synthesis","synthesize","ConfidenceAssessment","assess_confidence"]
