"""Local, organization, and federated search endpoints with BM25 ranking and verification badges."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, Query

from knowmesh_api.dependencies import PrincipalContext, get_service, require_permission
from knowmesh_api.schemas import SearchRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.post("")
def search_post(
    body: SearchRequest,
    principal: PrincipalContext = Depends(require_permission("knowledge:search")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    include_priv = not principal.authenticated and body.scope != "federated"
    return service.search(
        body.query,
        limit=body.limit,
        offset=body.offset,
        scope=body.scope,
        category=body.category,
        node_id=body.node_id,
        verification_state=body.verification_state,
        evidence_required=body.evidence_required,
        visibility=body.visibility,
        sort_by=body.sort_by,
        requester_org_id=principal.organization_id,
        include_private=include_priv,
    )


@router.get("")
def search_get(
    q: str = Query(..., min_length=1, max_length=2000),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    scope: str = Query("local"),
    category: str | None = None,
    node_id: str | None = None,
    verification_state: str | None = None,
    evidence_required: bool = False,
    visibility: str | None = None,
    sort_by: str = Query("relevance"),
    principal: PrincipalContext = Depends(require_permission("knowledge:search")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    include_priv = not principal.authenticated and scope != "federated"
    return service.search(
        q,
        limit=limit,
        offset=offset,
        scope=scope,
        category=category,
        node_id=node_id,
        verification_state=verification_state,
        evidence_required=evidence_required,
        visibility=visibility,
        sort_by=sort_by,
        requester_org_id=principal.organization_id,
        include_private=include_priv,
    )
