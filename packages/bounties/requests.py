"""Bounty request definitions and lifecycle state management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


class BountyError(ValueError):
    """Raised when a bounty request or operation is invalid."""


class BountyStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    AWARDED = "awarded"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class BountyRequest:
    bounty_id: str
    title: str
    domain: str
    requester_id: str
    reward_points: float = 10.0
    required_capabilities: tuple[str, ...] = ()
    minimum_reputation: float = 0.0
    minimum_evidence_count: int = 1
    status: BountyStatus = BountyStatus.OPEN
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.bounty_id or not self.bounty_id.strip():
            raise BountyError("bounty_id is required")
        if not self.title or not self.title.strip():
            raise BountyError("title is required")
        if not self.domain or not self.domain.strip():
            raise BountyError("domain is required")
        if not self.requester_id or not self.requester_id.strip():
            raise BountyError("requester_id is required")
        if self.reward_points < 0:
            raise BountyError("reward_points must be non-negative")
        if not 0.0 <= self.minimum_reputation <= 1.0:
            raise BountyError("minimum_reputation must be between 0 and 1")
        if self.minimum_evidence_count < 0:
            raise BountyError("minimum_evidence_count must be non-negative")
        if self.created_at.tzinfo is None:
            raise BountyError("created_at must be timezone-aware")
        if self.expires_at is not None and self.expires_at.tzinfo is None:
            raise BountyError("expires_at must be timezone-aware")
        object.__setattr__(self, "status", BountyStatus(self.status))

    def is_active(self, now: datetime | None = None) -> bool:
        if self.status not in {BountyStatus.OPEN, BountyStatus.IN_PROGRESS}:
            return False
        current = now or datetime.now(timezone.utc)
        if self.expires_at is not None and current >= self.expires_at:
            return False
        return True

    def with_status(self, status: BountyStatus) -> "BountyRequest":
        return BountyRequest(
            bounty_id=self.bounty_id,
            title=self.title,
            domain=self.domain,
            requester_id=self.requester_id,
            reward_points=self.reward_points,
            required_capabilities=self.required_capabilities,
            minimum_reputation=self.minimum_reputation,
            minimum_evidence_count=self.minimum_evidence_count,
            status=BountyStatus(status),
            description=self.description,
            created_at=self.created_at,
            expires_at=self.expires_at,
            metadata=self.metadata,
        )

