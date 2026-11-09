from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .identity import Identity


class Operation(Base, UUIDMixin, TimestampMixin):
    """Operation audit ledger recording actions executed across the knowledge mesh."""

    __tablename__ = "operations"
    __table_args__ = (
        Index("ix_operations_entity", "entity_type", "entity_id"),
    )

    operation_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # e.g., 'publish', 'verify', 'retract', 'challenge', 'mutate'
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # e.g., 'bundle', 'claim', 'evidence', 'verification'
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), default="completed", nullable=False, index=True
    )
    payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Relationships
    actor: Mapped[Optional["Identity"]] = relationship(
        "Identity",
        foreign_keys=[actor_id],
        lazy="selectin",
    )
