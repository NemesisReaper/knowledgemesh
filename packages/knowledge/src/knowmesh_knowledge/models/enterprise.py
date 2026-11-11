"""Multi-tenant organization, identity, agent, knowledge, federation, trust, and job models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    org_type: Mapped[str] = mapped_column(String(60), default="enterprise", nullable=False)
    settings_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Membership(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_user_membership"),
        Index("ix_membership_org_role", "organization_id", "role"),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), default="member", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class NodeRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "nodes"
    __table_args__ = (
        Index("ix_nodes_org_visibility", "organization_id", "visibility"),
    )

    node_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    hosting_type: Mapped[str] = mapped_column(String(50), default="self-hosted", nullable=False)
    visibility: Mapped[str] = mapped_column(String(40), default="organization", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False, index=True)
    capabilities_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    public_key: Mapped[str] = mapped_column(String(512), nullable=False)
    key_fingerprint: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class NodeKey(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "node_keys"

    node_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("nodes.node_id", ondelete="CASCADE"), nullable=False, index=True
    )
    algorithm: Mapped[str] = mapped_column(String(40), default="Ed25519", nullable=False)
    public_key: Mapped[str] = mapped_column(String(512), nullable=False)
    private_key_secret: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    key_fingerprint: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AgentRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agents"
    __table_args__ = (
        Index("ix_agents_org_node", "organization_id", "node_id"),
    )

    agent_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    node_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("nodes.node_id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    permissions_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class CredentialRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "credentials"

    credential_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    agent_id: Mapped[Optional[str]] = mapped_column(
        String(128), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=True, index=True
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    key_prefix: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    secret_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    permissions_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class KnowledgeCollection(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_collections"

    collection_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    category: Mapped[str] = mapped_column(String(100), default="general", nullable=False)


class KnowledgeBundleRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_bundles"
    __table_args__ = (
        Index("ix_kb_org_visibility_status", "organization_id", "visibility", "status"),
    )

    bundle_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), default="general", nullable=False, index=True)
    tags_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    collection_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    publisher_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    origin_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    visibility: Mapped[str] = mapped_column(String(40), default="organization", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False, index=True)
    current_revision: Mapped[str] = mapped_column(String(64), default="1.0.0", nullable=False)
    current_digest: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class KnowledgeRevisionRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_revisions"
    __table_args__ = (
        UniqueConstraint("bundle_id", "revision", name="uq_kb_bundle_revision"),
        Index("ix_kr_bundle_created", "bundle_id", "created_at"),
    )

    revision_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    bundle_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("knowledge_bundles.bundle_id", ondelete="CASCADE"), nullable=False, index=True
    )
    revision: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_revision: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    previous_digest: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    content_digest: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    merkle_root: Mapped[str] = mapped_column(String(128), nullable=False)
    publisher_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    signer_id: Mapped[str] = mapped_column(String(128), nullable=False)
    key_fingerprint: Mapped[str] = mapped_column(String(128), nullable=False)
    signature_envelope_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    okf_manifest_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    change_note: Mapped[str] = mapped_column(Text, default="", nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ClaimRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "claim_records"
    __table_args__ = (
        Index("ix_claim_records_bundle_status", "bundle_id", "status"),
    )

    claim_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    bundle_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    revision: Mapped[str] = mapped_column(String(64), default="1.0.0", nullable=False)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    claim_type: Mapped[str] = mapped_column(String(60), default="factual", nullable=False)
    domain: Mapped[str] = mapped_column(String(120), default="general", nullable=False, index=True)
    subject: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    predicate: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    object_val: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="proposed", nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    supporting_evidence_ids_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    contradictory_evidence_ids_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    source_references_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class EvidenceRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evidence_records"

    evidence_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    bundle_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    source_uri: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(60), default="reference", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    reliability: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    relation_type: Mapped[str] = mapped_column(String(40), default="supports", nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class SourceReference(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "source_references"

    source_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    uri: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    publisher: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    content_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProvenanceEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "provenance_events"
    __table_args__ = (
        Index("ix_prov_subject_ts", "subject_id", "occurred_at"),
    )

    record_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    subject_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    previous_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    record_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    details_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class PeerConnection(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "peer_connections"
    __table_args__ = (
        UniqueConstraint("local_node_id", "peer_node_id", name="uq_local_peer_node"),
    )

    peer_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    local_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    peer_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    public_key: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    key_fingerprint: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False, index=True)
    trust_level: Mapped[str] = mapped_column(String(40), default="standard", nullable=False)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    capabilities_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class PeerCapabilityRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "peer_capabilities"

    peer_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("peer_connections.peer_id", ondelete="CASCADE"), nullable=False, index=True
    )
    capability_name: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(40), default="1.0", nullable=False)


class SyncRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sync_records"
    __table_args__ = (
        Index("ix_sync_local_peer", "local_node_id", "peer_node_id"),
    )

    sync_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    local_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    peer_node_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    bundles_pulled: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bundles_unchanged: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conflicts_detected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    details_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class AccessPolicyRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "access_policies"

    policy_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    node_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
    permission: Mapped[str] = mapped_column(String(80), nullable=False)
    effect: Mapped[str] = mapped_column(String(20), default="allow", nullable=False)
    minimum_trust_level: Mapped[str] = mapped_column(String(40), default="standard", nullable=False)
    require_signature: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    require_provenance: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AuditEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "audit_events"
    __table_args__ = (
        Index("ix_audit_org_cat_ts", "organization_id", "category", "created_at"),
    )

    event_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    node_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    actor_type: Mapped[str] = mapped_column(String(50), default="user", nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(80), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=False)
    outcome: Mapped[str] = mapped_column(String(40), default="succeeded", nullable=False, index=True)
    request_id: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    details_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class BackgroundJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "background_jobs"
    __table_args__ = (
        Index("ix_bg_jobs_status_type", "status", "job_type"),
    )

    job_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True, index=True)
    job_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    node_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", nullable=False, index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    output_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    errors_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

