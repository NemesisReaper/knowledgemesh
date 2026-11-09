from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, UUIDMixin, TimestampMixin


class Evidence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evidence"

    source_uri: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)


class ClaimEvidence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "claim_evidence"
    __table_args__ = (
        UniqueConstraint("claim_id", "evidence_id", "relationship", name="uq_claim_evidence"),
    )

    claim_id: Mapped[UUID] = mapped_column(ForeignKey("claims.id"), nullable=False)
    evidence_id: Mapped[UUID] = mapped_column(ForeignKey("evidence.id"), nullable=False)
    relationship: Mapped[str] = mapped_column(String(40), nullable=False)


# Backward compatibility alias
ClaimEvidece = ClaimEvidence  # Deprecated misspelling retained for compatibility
