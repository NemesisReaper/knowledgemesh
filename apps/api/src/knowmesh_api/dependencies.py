"""FastAPI dependency injection for KnowMeshService, authentication, and RBAC."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from fastapi import Depends, HTTPException, Request

from .security import ROLE_PERMISSIONS, verify_signed_token
from .service import KnowMeshService


@dataclass(slots=True)
class PrincipalContext:
    actor_id: str = "system"
    actor_type: str = "anonymous"
    organization_id: str | None = None
    node_id: str | None = None
    role: str = "owner"
    permissions: frozenset[str] = field(default_factory=lambda: ROLE_PERMISSIONS["owner"])
    authenticated: bool = False
    raw_token: str | None = None


def get_service(request: Request) -> KnowMeshService:
    svc = getattr(request.app.state, "service", None)
    if svc is None:
        svc = KnowMeshService()
        request.app.state.service = svc
    return svc


def get_optional_principal(
    request: Request,
    service: KnowMeshService = Depends(get_service),
) -> PrincipalContext:
    api_key = request.headers.get("X-KnowMesh-Key", "").strip()
    auth_header = request.headers.get("Authorization", "").strip()

    if auth_header.lower().startswith("bearer "):
        token = auth_header[7:].strip()
        if token.startswith("km_live_"):
            api_key = token
        elif token:
            try:
                payload = verify_signed_token(
                    token,
                    secret_key=service.settings.secret_key,
                    expected_type="access",
                    revocation_store=service.token_revocations,
                )
            except (PermissionError, ValueError) as exc:
                raise HTTPException(status_code=401, detail=str(exc)) from exc
            role = str(payload.get("role") or "member")
            perms = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["member"])
            return PrincipalContext(
                actor_id=str(payload["sub"]),
                actor_type="user",
                organization_id=payload.get("org_id"),
                node_id=service.settings.node_id,
                role=role,
                permissions=perms,
                authenticated=True,
                raw_token=token,
            )

    if api_key:
        try:
            cred_ctx = service.authenticate_credential(api_key)
        except PermissionError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        return PrincipalContext(
            actor_id=str(cred_ctx["actor_id"]),
            actor_type="agent",
            organization_id=cred_ctx.get("organization_id"),
            node_id=cred_ctx.get("node_id"),
            role="agent",
            permissions=frozenset(cred_ctx.get("permissions") or []),
            authenticated=True,
        )

    org_header = request.headers.get("X-KnowMesh-Org", "").strip() or None
    return PrincipalContext(
        actor_id="system",
        actor_type="anonymous",
        organization_id=org_header,
        node_id=service.settings.node_id,
        role="owner",
        permissions=ROLE_PERMISSIONS["owner"],
        authenticated=False,
    )


def require_authenticated(
    principal: PrincipalContext = Depends(get_optional_principal),
) -> PrincipalContext:
    if not principal.authenticated:
        raise HTTPException(status_code=401, detail="Authentication required")
    return principal


def require_permission(permission: str, *, allow_unauthenticated_local: bool = True) -> Callable[..., PrincipalContext]:
    def _dep(principal: PrincipalContext = Depends(get_optional_principal)) -> PrincipalContext:
        if not principal.authenticated and allow_unauthenticated_local:
            return principal
        if not principal.authenticated:
            raise HTTPException(status_code=401, detail="Authentication required")
        if permission not in principal.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Principal {principal.actor_id!r} ({principal.role}) lacks required permission {permission!r}",
            )
        return principal

    return _dep
