"""KnowMesh API v1 router combining organization console, developer platform, and federation endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query

from ...dependencies import (
    PrincipalContext,
    get_optional_principal,
    get_service,
    require_authenticated,
    require_permission,
)
from ...schemas import (
    AccessPolicyCreateRequest,
    AgentCreateRequest,
    AgentPermissionsUpdateRequest,
    CredentialCreateRequest,
    JobEnqueueRequest,
    LoginRequest,
    MemberAddRequest,
    OrganizationCreateRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from ...service import KnowMeshService
from .endpoints import (
    bounties,
    bundles,
    challenges,
    claims,
    discovery,
    evidence,
    evolution,
    experiments,
    federation,
    nodes,
    reputation,
    search,
    simulations,
    subscriptions,
)

api_router = APIRouter()

# Core domain routers
api_router.include_router(bundles.router, prefix="/bundles", tags=["bundles"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
api_router.include_router(nodes.router, prefix="/nodes", tags=["nodes"])
api_router.include_router(federation.router, prefix="/federation", tags=["federation"])
api_router.include_router(federation.router, prefix="/peers", tags=["peers"])
api_router.include_router(discovery.router, prefix="/discovery", tags=["discovery"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(reputation.router, prefix="/reputation", tags=["reputation"])
api_router.include_router(evolution.router, prefix="/evolution", tags=["evolution"])
api_router.include_router(bounties.router, prefix="/bounties", tags=["bounties"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(simulations.router, prefix="/simulations", tags=["simulations"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])

# ------------------------------------------------------------------
# 4.1 Authentication & Session Endpoints (/auth)
# ------------------------------------------------------------------
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201)
def register_user(
    body: RegisterRequest,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.register_user(
            email=body.email,
            password=body.password,
            full_name=body.full_name,
            organization_name=body.organization_name,
            organization_slug=body.organization_slug,
            organization_type=body.organization_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@auth_router.post("/login")
def login_user(
    body: LoginRequest,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.authenticate_user(email=body.email, password=body.password)
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@auth_router.post("/demo-bypass")
def demo_bypass(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    """Instant demo bypass for interactive evaluation of the KnowMesh console."""
    demo_email = "demo@knowmesh.local"
    demo_pass = "demo12345"
    try:
        return service.authenticate_user(email=demo_email, password=demo_pass)
    except PermissionError:
        # Create demo account on-the-fly using standard service registration
        return service.register_user(
            email=demo_email,
            password=demo_pass,
            full_name="Lead Curator & Mesh Administrator",
            organization_name="Sovereign AI Safety Mesh",
            organization_slug="sovereign-ai-safety",
            organization_type="foundation",
        )


@auth_router.post("/refresh")
def refresh_token(
    body: RefreshTokenRequest,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.refresh_session(body.refresh_token)
    except (PermissionError, ValueError) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@auth_router.post("/logout")
def logout_user(
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    if principal.raw_token:
        service.revoke_session_token(principal.raw_token)
    return {"status": "revoked"}


@auth_router.get("/me")
def get_current_principal(
    principal: PrincipalContext = Depends(require_authenticated),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    orgs = service.list_organizations(user_id=principal.actor_id if principal.actor_type == "user" else None)
    return {
        "actor_id": principal.actor_id,
        "actor_type": principal.actor_type,
        "organization_id": principal.organization_id,
        "node_id": principal.node_id,
        "role": principal.role,
        "permissions": sorted(principal.permissions),
        "organizations": orgs,
    }


api_router.include_router(auth_router)

# ------------------------------------------------------------------
# 4.1 Organizations & Memberships (/organizations)
# ------------------------------------------------------------------
orgs_router = APIRouter(prefix="/organizations", tags=["organizations"])


@orgs_router.get("")
def list_organizations(
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_organizations(user_id=principal.actor_id if principal.actor_type == "user" else None)
    return {"items": items, "total": len(items)}


@orgs_router.post("", status_code=201)
def create_organization(
    body: OrganizationCreateRequest,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.create_organization(
            name=body.name,
            slug=body.slug,
            description=body.description,
            org_type=body.org_type,
            settings_data=body.settings,
            creator_user_id=principal.actor_id if principal.actor_type == "user" else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@orgs_router.get("/{organization_id}/members")
def list_organization_members(
    organization_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        items = service.list_organization_members(organization_id)
        return {"items": items, "total": len(items)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@orgs_router.post("/{organization_id}/members", status_code=201)
def add_organization_member(
    organization_id: str,
    body: MemberAddRequest,
    principal: PrincipalContext = Depends(require_permission("organization:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.add_organization_member(
            organization_id,
            email=body.email,
            full_name=body.full_name,
            role=body.role,
            password=body.password,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


api_router.include_router(orgs_router)

# ------------------------------------------------------------------
# 4.3 Agent Identity & Credentials (/agents & /credentials)
# ------------------------------------------------------------------
agents_router = APIRouter(prefix="/agents", tags=["agents"])


@agents_router.get("")
def list_agents(
    organization_id: str | None = None,
    node_id: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_agents(organization_id=organization_id, node_id=node_id)
    return {"items": items, "total": len(items)}


@agents_router.post("", status_code=201)
def register_agent(
    body: AgentCreateRequest,
    principal: PrincipalContext = Depends(require_permission("agent:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.register_agent(
            agent_id=body.agent_id,
            name=body.name,
            description=body.description,
            organization_id=body.organization_id or principal.organization_id,
            node_id=body.node_id,
            permissions=body.permissions,
            issue_initial_credential=body.issue_initial_credential,
            metadata=body.metadata,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@agents_router.get("/{agent_id}")
def get_agent(
    agent_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@agents_router.patch("/{agent_id}/permissions")
def update_agent_permissions(
    agent_id: str,
    body: AgentPermissionsUpdateRequest,
    principal: PrincipalContext = Depends(require_permission("agent:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.update_agent_permissions(
            agent_id,
            permissions=body.permissions,
            status=body.status,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


api_router.include_router(agents_router)

creds_router = APIRouter(prefix="/credentials", tags=["credentials"])


@creds_router.get("")
def list_credentials(
    organization_id: str | None = None,
    agent_id: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_credentials(organization_id=organization_id, agent_id=agent_id)
    return {"items": items, "total": len(items)}


@creds_router.post("", status_code=201)
def issue_credential(
    body: CredentialCreateRequest,
    principal: PrincipalContext = Depends(require_permission("credential:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.issue_credential(
            name=body.name,
            agent_id=body.agent_id,
            organization_id=body.organization_id or principal.organization_id,
            permissions=body.permissions,
            expires_in_days=body.expires_in_days,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@creds_router.post("/{credential_id}/rotate")
def rotate_credential(
    credential_id: str,
    principal: PrincipalContext = Depends(require_permission("credential:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.rotate_credential(credential_id, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@creds_router.post("/{credential_id}/revoke")
def revoke_credential(
    credential_id: str,
    principal: PrincipalContext = Depends(require_permission("credential:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.revoke_credential(credential_id, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


api_router.include_router(creds_router)

# ------------------------------------------------------------------
# 4.4 OKF Validation & 4.6 Trust/Signature Verification (/okf & /trust)
# ------------------------------------------------------------------
okf_router = APIRouter(prefix="/okf", tags=["okf"])


@okf_router.post("/validate")
def validate_okf_manifest(
    body: dict[str, Any],
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.validate_okf(body)


api_router.include_router(okf_router)

trust_router = APIRouter(prefix="/trust", tags=["trust"])


@trust_router.post("/verify")
def verify_bundle_or_payload(
    body: dict[str, Any],
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    if "bundle_id" in body and "okf_manifest" not in body and "signature" not in body and "claims" not in body:
        try:
            bundle = service.get_bundle(
                str(body["bundle_id"]),
                revision=body.get("revision"),
                include_private=True,
            )
            return bundle["verification"]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    return service.verify_bundle_payload(body, public_key=body.get("public_key"))


@trust_router.get("/policies")
def list_access_policies(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_access_policies()
    return {"items": items, "total": len(items)}


@trust_router.post("/policies", status_code=201)
def create_access_policy(
    body: AccessPolicyCreateRequest,
    principal: PrincipalContext = Depends(require_permission("organization:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.create_access_policy(
        name=body.name,
        organization_id=body.organization_id or principal.organization_id,
        node_id=body.node_id,
        role=body.role,
        permission=body.permission,
        effect=body.effect,
        minimum_trust_level=body.minimum_trust_level,
        require_signature=body.require_signature,
        require_provenance=body.require_provenance,
        actor_id=principal.actor_id,
    )


@trust_router.get("/revocations")
def list_revocations(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    recs = [
        {
            "subject_id": r.subject_id,
            "reason": r.reason,
            "revoked_by": r.revoked_by,
            "key_fingerprint": r.key_fingerprint,
            "revoked_at": r.revoked_at.isoformat(),
        }
        for r in service.revocation_registry.records()
    ]
    return {"items": recs, "total": len(recs)}


api_router.include_router(trust_router)

# ------------------------------------------------------------------
# 4.12 & 4.14 Overview, Audit Logs, Background Jobs (/overview, /audit, /jobs)
# ------------------------------------------------------------------
@api_router.post("/demo/bootstrap", tags=["demo"])
def bootstrap_demo(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.bootstrap_demo_state()


@api_router.get("/overview", tags=["overview"])
def get_overview_dashboard(
    organization_id: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.get_overview_metrics(organization_id=organization_id)


@api_router.get("/audit", tags=["audit"])
def list_audit_events(
    category: str | None = None,
    actor_id: str | None = None,
    node_id: str | None = None,
    outcome: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_audit_events(
        category=category,
        actor_id=actor_id,
        node_id=node_id,
        outcome=outcome,
        limit=limit,
    )
    return {"items": items, "total": len(items)}


jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])


@jobs_router.get("")
def list_background_jobs(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_jobs()
    return {"items": items, "total": len(items)}


@jobs_router.post("", status_code=201)
def enqueue_background_job(
    body: JobEnqueueRequest,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.enqueue_job(
        body.job_type,
        body.payload,
        idempotency_key=body.idempotency_key,
        execute_immediately=body.execute_immediately,
    )


api_router.include_router(jobs_router)
