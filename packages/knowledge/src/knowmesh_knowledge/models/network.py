from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .identity import PublisherIdentity


class NetworkNode(Base, UUIDMixin, TimestampMixin):
    """Federation peer node registered in the KnowledgeMesh network."""

    __tablename__ = "network_nodes"

    node_id: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=False
    )
    endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "publisher_identities.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_network_nodes_identity_id",
        ),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), default="active", nullable=False, index=True
    )
    capabilities: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    identity: Mapped[Optional["PublisherIdentity"]] = relationship(
        "PublisherIdentity",
        foreign_keys=[identity_id],
        lazy="selectin",
    )
