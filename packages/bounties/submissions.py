"""Bounty submissions linking candidate knowledge bundles and evidence to a bounty request."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

from .requests import BountyError


class SubmissionStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class BountySubmission:
    submission_id: str
    bounty_id: str
    contributor_id: str
    bundle_id: str
    claim_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.8
    signature_verified: bool = False
    status: SubmissionStatus = SubmissionStatus.SUBMITTED
    submitted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    notes: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.submission_id or not self.bounty_id or not self.contributor_id or not self.bundle_id:
            raise BountyError("submission_id, bounty_id, contributor_id, and bundle_id are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise BountyError("confidence must be between 0 and 1")
        if self.submitted_at.tzinfo is None:
            raise BountyError("submitted_at must be timezone-aware")
        object.__setattr__(self, "status", SubmissionStatus(self.status))

