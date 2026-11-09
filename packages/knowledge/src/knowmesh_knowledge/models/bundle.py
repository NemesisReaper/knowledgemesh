from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSON
from .base import Base, UUIDMixin, TimestampMixin

class Bundle(Base,UUIDMixin,TimestampMixin):
    __tablename__="bundles"
    publisher_id: Mapped[UUID]=mapped_column(ForeignKey("publisher_identities.id"),nullable=False,index=True)
    bundle_identifier: Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    title: Mapped[str]=mapped_column(String(300),nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    visibility: Mapped[str] = mapped_column(String(30), default="public", nullable=False)

class BundleVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bundle_versions"
    __table_args__ = (UniqueConstraint("bundle_id", "version", name="uq_bundle_version"),)
    bundle_id: Mapped[UUID] = mapped_column(ForeignKey("bundles.id"), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    digest: Mapped[str] = mapped_column(String(128), nullable=False)
    signature: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    manifest: Mapped[dict]=mapped_column(JSON,nullable=False)
    format_version: Mapped[str]=mapped_column(String(30),default="0.2",nullable=False)