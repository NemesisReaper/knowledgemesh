"""Pydantic v2 API schemas for KnowMesh Organization Console, Developer Platform, and Federation Protocol."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    id: str | None = None
    name: str | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    domain: str | None = None
    category: str | None = None
    visibility: str | None = None
    publisher_node_id: str | None = None
    organization_id: str | None = None
    claims: list[dict[str, Any]] | None = None
    evidence: list[dict[str, Any]] | None = None
    tags: list[str] | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: str = "active"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    scope: str = Field(default="local")  # local | organization | federated
    category: str | None = None
    node_id: str | None = None
    verification_state: str | None = None
    evidence_required: bool = False
    visibility: str | None = None
    sort_by: str = Field(default="relevance")  # relevance | freshness


class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=256)
    full_name: str = Field(min_length=1, max_length=200)
    organization_name: str | None = None
    organization_slug: str | None = None
    organization_type: str = "enterprise"


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class OrganizationCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str | None = None
    description: str = ""
    org_type: str = "enterprise"
    settings: dict[str, Any] = Field(default_factory=dict)


class MemberAddRequest(BaseModel):
    email: str
    full_name: str = "Organization Member"
    role: str = "member"
    password: str | None = None


class NodeCreateRequest(BaseModel):
    node_id: str | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    organization_id: str | None = None
    endpoint: str = "http://127.0.0.1:8000"
    hosting_type: str = "self-hosted"
    visibility: str = "organization"  # private | organization | federated
    capabilities: list[str] = Field(
        default_factory=lambda: ["knowledge:publish", "knowledge:search", "federation:sync", "trust:ed25519"]
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class NodeUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    endpoint: str | None = None
    visibility: str | None = None
    capabilities: list[str] | None = None
    status: str | None = None
    metadata: dict[str, Any] | None = None


class AgentCreateRequest(BaseModel):
    agent_id: str | None = None
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    organization_id: str | None = None
    node_id: str | None = None
    permissions: list[str] = Field(
        default_factory=lambda: ["knowledge:read", "knowledge:search", "verification:read"]
    )
    issue_initial_credential: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentPermissionsUpdateRequest(BaseModel):
    permissions: list[str]
    status: str | None = None


class CredentialCreateRequest(BaseModel):
    name: str = "Default Agent Key"
    agent_id: str | None = None
    organization_id: str | None = None
    permissions: list[str] | None = None
    expires_in_days: int | None = 90


class ClaimInput(BaseModel):
    claim_id: str | None = None
    statement: str
    claim_type: str = "factual"
    domain: str = "general"
    subject: str | None = None
    predicate: str | None = None
    object: str | None = None
    status: str = "proposed"
    evidence_ids: list[str] = Field(default_factory=list)
    contradictory_evidence_ids: list[str] = Field(default_factory=list)
    source_references: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvidenceInput(BaseModel):
    evidence_id: str | None = None
    title: str = ""
    source_uri: str = "https://knowmesh.org/sources/primary"
    source_type: str = "reference"
    description: str = ""
    content_hash: str = ""
    reliability: float = Field(default=0.85, ge=0.0, le=1.0)
    relation_type: str = "supports"
    metadata: dict[str, Any] = Field(default_factory=dict)


class BundleCreateRequest(BaseModel):
    id: str | None = None
    bundle_id: str | None = None
    title: str = Field(min_length=1, max_length=300)
    description: str = ""
    content: str = ""
    category: str = "general"
    tags: list[str] = Field(default_factory=list)
    collection_id: str | None = None
    organization_id: str | None = None
    node_id: str | None = None
    visibility: str = "federated"  # private | organization | federated
    version: str = "1.0.0"
    publish: bool = True
    claims: list[ClaimInput | dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceInput | dict[str, Any]] = Field(default_factory=list)
    links: list[dict[str, Any]] = Field(default_factory=list)
    change_note: str = "Initial publication"
    metadata: dict[str, Any] = Field(default_factory=dict)


class BundleRevisionRequest(BaseModel):
    version: str | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    visibility: str | None = None
    claims: list[ClaimInput | dict[str, Any]] | None = None
    evidence: list[EvidenceInput | dict[str, Any]] | None = None
    links: list[dict[str, Any]] | None = None
    change_note: str = "Knowledge revision update"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClaimStatusUpdateRequest(BaseModel):
    status: str
    reason: str = ""


class PeerRegisterRequest(BaseModel):
    peer_node_id: str | None = None
    name: str
    endpoint: str
    public_key: str = ""
    key_fingerprint: str = ""
    capabilities: list[str] = Field(default_factory=lambda: ["knowledge:search", "federation:sync"])
    trust_level: str = "standard"
    auto_approve: bool = False


class AccessPolicyCreateRequest(BaseModel):
    name: str
    organization_id: str | None = None
    node_id: str | None = None
    role: str = "curator"
    permission: str = "knowledge:publish"
    effect: str = "allow"
    minimum_trust_level: str = "standard"
    require_signature: bool = True
    require_provenance: bool = True


class JobEnqueueRequest(BaseModel):
    job_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None
    execute_immediately: bool = True
