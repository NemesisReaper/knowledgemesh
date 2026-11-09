from uuid import UUID
from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TSVECTOR, JSON
from .base import Base, UUIDMixin, TimestampMixin
from .bundle import BundleVersion

class Claim(Base,UUIDMixin,TimestampMixin):
    __tablename__="claims"
    __table_args__=(Index("ix_claim_domain_status","domain", "status"),)
    bundle_version_id: Mapped[UUID]=mapped_column(ForeignKey("bundle_versions.id"),nullable=False,index=True)
    statement: Mapped[str]=mapped_column(Text,nullable=False)
    domain: Mapped[str]=mapped_column(String(150),nullable=False)
    claim_type: Mapped[str]=mapped_column(String(50), default="factual", nullable=False)
    status: Mapped[str]=mapped_column(String(40), default="proposed", nullable=False)
    metadata_json: Mapped[dict]=mapped_column(JSON, default=dict, nullable=False)

    
    