from __future__ import annotations

from uuid import UUID

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, UUIDMixin, TimestampMixin


class PublisherIdentity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "publisher_identities"

    node_id: Mapped[UUID] = mapped_column(ForeignKey("network_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    public_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    key_fingerprint: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


# Alias
Identity = PublisherIdentity
