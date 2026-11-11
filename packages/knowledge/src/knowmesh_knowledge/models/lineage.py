from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy import JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .bundle import Bundle
    from .identity import PublisherIdentity


class Lineage(Base, UUIDMixin, TimestampMixin):
    """Knowledge lineage tracking evolutionary operations (mutations, splits, merges, derivations)."""

    __tablename__ = "lineages"
    __table_args__ = (
        Index("ix_lineage_parent_child", "parent_bundle_id", "child_bundle_id"),
    )

    parent_bundle_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("bundles.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    child_bundle_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("bundles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    operation: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # e.g., 'mutation', 'split', 'merge', 'derivation'
    diff_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("publisher_identities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata", JSON, nullable=True
    )

    # Relationships
    parent_bundle: Mapped[Optional["Bundle"]] = relationship(
        "Bundle",
        foreign_keys=[parent_bundle_id],
        lazy="selectin",
    )
    child_bundle: Mapped["Bundle"] = relationship(
        "Bundle",
        foreign_keys=[child_bundle_id],
        lazy="selectin",
    )
    actor: Mapped[Optional["PublisherIdentity"]] = relationship(
        "PublisherIdentity",
        foreign_keys=[actor_id],
        lazy="selectin",
    )
