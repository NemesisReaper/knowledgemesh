"""Knowledge bundle, OKF manifest, revision, provenance, and knowledge graph endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query

from knowmesh_api.dependencies import PrincipalContext, get_optional_principal, get_service, require_permission
from knowmesh_api.schemas import BundleCreateRequest, BundleRevisionRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.get("")
def list_bundles(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = None,
    status: str | None = None,
    visibility: str | None = None,
    category: str | None = None,
    organization_id: str | None = None,
    principal: PrincipalContext = Depends(require_permission("knowledge:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    effective_org = organization_id or principal.organization_id
    include_priv = not principal.authenticated or principal.role in {"owner", "admin", "curator"}
    items = service.list_bundles(
        limit=limit,
        offset=offset,
        query=q,
        status=status,
        visibility=visibility,
        category=category,
        organization_id=effective_org,
        include_private=include_priv and effective_org is None,
    )
    return {"items": items, "limit": limit, "offset": offset, "total": len(items)}


@router.post("", status_code=201)
def create_bundle(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("knowledge:publish")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    req = BundleCreateRequest.model_validate({
        "bundle_id": body.get("bundle_id") or body.get("id"),
        "title": body.get("title") or body.get("name") or "Untitled Knowledge Bundle",
        "description": body.get("description") or "",
        "content": body.get("content") or "",
        "category": body.get("category") or body.get("domain") or "general",
        "tags": body.get("tags") or [],
        "collection_id": body.get("collection_id"),
        "organization_id": body.get("organization_id") or principal.organization_id,
        "node_id": body.get("node_id") or body.get("publisher_node_id") or principal.node_id,
        "visibility": body.get("visibility") or "federated",
        "version": body.get("version") or "1.0.0",
        "publish": body.get("publish", True),
        "claims": body.get("claims") or [],
        "evidence": body.get("evidence") or [],
        "links": body.get("links") or [],
        "change_note": body.get("change_note") or "Initial publication",
        "metadata": body.get("metadata") or body.get("payload") or {},
    })
    try:
        return service.create_or_publish_bundle(
            bundle_id=req.bundle_id,
            title=req.title,
            description=req.description,
            content=req.content,
            category=req.category,
            tags=req.tags,
            collection_id=req.collection_id,
            organization_id=req.organization_id,
            node_id=req.node_id,
            visibility=req.visibility,
            version=req.version,
            publish=req.publish,
            claims=[c if isinstance(c, dict) else c.model_dump() for c in req.claims],
            evidence=[e if isinstance(e, dict) else e.model_dump() for e in req.evidence],
            links=req.links,
            change_note=req.change_note,
            metadata=req.metadata,
            actor_id=principal.actor_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{bundle_id}")
def get_bundle(
    bundle_id: str,
    revision: str | None = None,
    principal: PrincipalContext = Depends(require_permission("knowledge:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    include_priv = not principal.authenticated and principal.organization_id is None
    try:
        return service.get_bundle(
            bundle_id,
            revision=revision,
            requester_org_id=principal.organization_id,
            include_private=include_priv,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"bundles record not found: {bundle_id}") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/{bundle_id}/revisions", status_code=201)
def publish_revision(
    bundle_id: str,
    body: BundleRevisionRequest,
    principal: PrincipalContext = Depends(require_permission("knowledge:update")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.publish_bundle_revision(
            bundle_id,
            version=body.version,
            title=body.title,
            description=body.description,
            content=body.content,
            visibility=body.visibility,
            claims=[c if isinstance(c, dict) else c.model_dump() for c in body.claims] if body.claims is not None else None,
            evidence=[e if isinstance(e, dict) else e.model_dump() for e in body.evidence] if body.evidence is not None else None,
            links=body.links,
            change_note=body.change_note,
            metadata=body.metadata,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{bundle_id}/revisions")
def list_bundle_revisions(
    bundle_id: str,
    principal: PrincipalContext = Depends(require_permission("knowledge:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        bundle = service.get_bundle(
            bundle_id,
            requester_org_id=principal.organization_id,
            include_private=not principal.authenticated,
        )
        return {"bundle_id": bundle_id, "current_revision": bundle["current_revision"], "items": bundle["revisions"]}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.get("/{bundle_id}/diff")
def diff_bundle_revisions(
    bundle_id: str,
    from_rev: str = Query(..., description="Base revision"),
    to_rev: str = Query(..., description="Target revision"),
    principal: PrincipalContext = Depends(require_permission("knowledge:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.compare_revisions(bundle_id, from_rev, to_rev)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{bundle_id}/provenance")
def get_bundle_provenance(
    bundle_id: str,
    principal: PrincipalContext = Depends(require_permission("verification:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        bundle = service.get_bundle(
            bundle_id,
            requester_org_id=principal.organization_id,
            include_private=not principal.authenticated,
        )
        return {
            "bundle_id": bundle_id,
            "verification": bundle["verification"],
            "provenance": bundle["provenance"],
        }
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.get("/{bundle_id}/graph")
def get_bundle_graph(
    bundle_id: str,
    principal: PrincipalContext = Depends(require_permission("knowledge:read")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.build_bundle_graph(bundle_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{bundle_id}/archive")
def archive_bundle(
    bundle_id: str,
    withdraw: bool = Query(False),
    principal: PrincipalContext = Depends(require_permission("knowledge:update")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.archive_bundle(bundle_id, withdraw=withdraw, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{bundle_id}", status_code=204)
def delete_bundle(
    bundle_id: str,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> None:
    if not service.delete_bundle(bundle_id):
        raise HTTPException(status_code=404, detail="bundles record not found")
    return None
