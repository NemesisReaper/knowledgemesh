from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

class EvidenceRelation(str, Enum):
    SUPPORTS="supports"
    REFUTES="refutes"
    CONTEXTUALIZES="contextualizes"
    DERIVED_FROM="derived_from"

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    content: str
    source_uri: str = ""
    source_type: str = "document"
    publisher_id: str = ""
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reliability: float | None = None
    metadata: dict[str,Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.evidence_id.strip() or not self.content.strip():
            raise ValueError("evidence_id and content are required")
        if self.observed_at.tzinfo is None: raise ValueError("observed_at must be timezone-aware")
        if self.reliability is not None and not 0 <= self.reliability <= 1:
            raise ValueError("reliability must be between 0 and 1")

@dataclass(frozen=True)
class EvidenceAssessment:
    evidence_id: str
    claim_id: str
    relation: EvidenceRelation
    relevance: float = 1.0
    rationale: str = ""
    assessor_id: str = ""
    def __post_init__(self):
        if not 0 <= self.relevance <= 1: raise ValueError("relevance must be between 0 and 1")
