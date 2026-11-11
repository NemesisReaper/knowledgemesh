"""Federated discovery endpoint module."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends

from knowmesh_api.dependencies import PrincipalContext, get_service, require_permission
from knowmesh_api.schemas import SearchRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.post("")
def discover_knowledge(
    body: SearchRequest,
    principal: PrincipalContext = Depends(require_permission("federation:discover")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.search(
        body.query,
        limit=body.limit,
        offset=body.offset,
        scope="federated",
        category=body.category,
        node_id=body.node_id,
        verification_state=body.verification_state,
        evidence_required=body.evidence_required,
        visibility=body.visibility,
        sort_by=body.sort_by,
        requester_org_id=principal.organization_id,
        include_private=False,
    )
