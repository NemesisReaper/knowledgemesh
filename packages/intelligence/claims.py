from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

class ClaimStatus(str, Enum):
    PROPOSED="proposed"
    SUPPORTED="supported"
    CONTESTED="contested"
    INCONCLUSIVE="inconclusive"
    REJECTED="rejected"
    SUPERSEDED="superseded"

@dataclass(frozen=True)
class Claim:
    claim_id: str
    statement: str
    subject: str = ""
    predicate: str = ""
    object: str = ""
    status: ClaimStatus = ClaimStatus.PROPOSED
    evidence_ids: tuple[str,...] = ()
    source_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str,Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.claim_id.strip() or not self.statement.strip():
            raise ValueError("claim_id and statement are required")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
