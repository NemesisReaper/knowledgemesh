from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import CheckConstraint, Float, ForeignKey, Index, String, Text
from sqlalchemy import JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .bundle import Bundle
    from .claim import Claim
    from .identity import Identity


class Verification(Base, UUIDMixin, TimestampMixin):
    """Cryptographic attestation and verification record for claims or bundles."""

    __tablename__ = "verifications"
    __table_args__ = (
        CheckConstraint(
            "(claim_id IS NOT NULL AND bundle_id IS NULL) OR "
            "(claim_id IS NULL AND bundle_id IS NOT NULL)",
            name="ck_verification_exactly_one_target",
        ),
        Index("ix_verifications_target_claim", "claim_id", "verifier_id"),
        Index("ix_verifications_target_bundle", "bundle_id", "verifier_id"),
    )

    claim_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("claims.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("bundles.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    verifier_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("publisher_identities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outcome: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # 'verified', 'rejected', 'inconclusive'
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    signature: Mapped[str] = mapped_column(Text, nullable=False)
    algorithm: Mapped[str] = mapped_column(
        String(50), default="ed25519", nullable=False
    )
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata", JSON, nullable=True
    )

    # Relationships
    claim: Mapped[Optional["Claim"]] = relationship("Claim", foreign_keys=[claim_id], lazy="selectin")
    bundle: Mapped[Optional["Bundle"]] = relationship("Bundle", foreign_keys=[bundle_id], lazy="selectin")
    verifier: Mapped["Identity"] = relationship("Identity", foreign_keys=[verifier_id], lazy="selectin")
