"""Independent knowledge node registration, Ed25519 identity, capabilities, and key rotation endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from knowmesh_knowledge.models import NodeRecord

from knowmesh_api.dependencies import PrincipalContext, get_optional_principal, get_service, require_permission
from knowmesh_api.schemas import NodeCreateRequest, NodeUpdateRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.get("")
def list_nodes(
    organization_id: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_nodes(organization_id=organization_id)
    if q:
        ql = q.casefold()
        items = [i for i in items if ql in str(i).casefold()]
    return {"items": items[offset : offset + limit], "limit": limit, "offset": offset, "total": len(items)}


@router.post("", status_code=201)
def register_node(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("node:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    req = NodeCreateRequest.model_validate({
        "node_id": body.get("node_id") or body.get("id"),
        "name": body.get("name") or body.get("title") or "KnowMesh Node",
        "description": body.get("description") or "",
        "organization_id": body.get("organization_id") or principal.organization_id,
        "endpoint": body.get("endpoint") or service.settings.node_endpoint,
        "hosting_type": body.get("hosting_type") or "self-hosted",
        "visibility": body.get("visibility") or "organization",
        "capabilities": body.get("capabilities")
        or ["knowledge:publish", "knowledge:search", "federation:sync", "trust:ed25519"],
        "metadata": body.get("metadata") or body.get("payload") or {},
    })
    try:
        return service.register_node(
            node_id=req.node_id,
            name=req.name,
            description=req.description,
            organization_id=req.organization_id,
            endpoint=req.endpoint,
            hosting_type=req.hosting_type,
            visibility=req.visibility,
            capabilities=req.capabilities,
            metadata=req.metadata,
            actor_id=principal.actor_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{node_id}")
def get_node(
    node_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.get_node(node_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="nodes record not found") from exc


@router.patch("/{node_id}")
def update_node(
    node_id: str,
    body: NodeUpdateRequest,
    principal: PrincipalContext = Depends(require_permission("node:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.update_node(
            node_id,
            body.model_dump(exclude_none=True),
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{node_id}/identity")
def get_node_identity(
    node_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.get_node_public_identity(node_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{node_id}/rotate-key")
def rotate_node_key(
    node_id: str,
    reason: str = Query("scheduled rotation"),
    principal: PrincipalContext = Depends(require_permission("node:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.rotate_node_key(node_id, reason=reason, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{node_id}/health")
def get_node_health(
    node_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        node = service.get_node(node_id)
        report = service.health_registry.run().to_dict()
        return {
            "node_id": node["node_id"],
            "status": "healthy" if node["status"] == "active" else node["status"],
            "endpoint": node["endpoint"],
            "visibility": node["visibility"],
            "key_fingerprint": node["key_fingerprint"],
            "checks": report["checks"],
        }
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{node_id}", status_code=204)
def delete_node(
    node_id: str,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> None:
    with service.SessionLocal() as session:
        rec = session.scalar(select(NodeRecord).where(NodeRecord.node_id == node_id))
        if rec is None:
            raise HTTPException(status_code=404, detail="nodes record not found")
        session.delete(rec)
        session.commit()
    return None
