"""Evidence reference and provenance endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from knowmesh_knowledge.models import EvidenceRecord

from knowmesh_api.dependencies import PrincipalContext, get_optional_principal, get_service, require_permission
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.get("")
def list_evidence(
    bundle_id: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_evidence(bundle_id=bundle_id)
    if q:
        ql = q.casefold()
        items = [i for i in items if ql in str(i).casefold()]
    return {"items": items[offset : offset + limit], "limit": limit, "offset": offset, "total": len(items)}


@router.post("", status_code=201)
def create_evidence(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("knowledge:publish")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.create_evidence(
        evidence_id=body.get("evidence_id") or body.get("id"),
        bundle_id=body.get("bundle_id"),
        title=str(body.get("title") or body.get("name") or body.get("description") or "Evidence Record"),
        source_uri=str(body.get("source_uri") or "https://knowmesh.org/sources/primary"),
        source_type=str(body.get("source_type") or "reference"),
        description=str(body.get("description") or body.get("content") or ""),
        content_hash=str(body.get("content_hash") or ""),
        reliability=float(body.get("reliability", 0.85)),
        relation_type=str(body.get("relation_type") or "supports"),
        metadata=body.get("metadata") or body.get("payload") or {},
    )


@router.get("/{evidence_id}")
def get_evidence(
    evidence_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    with service.SessionLocal() as session:
        rec = session.scalar(select(EvidenceRecord).where(EvidenceRecord.evidence_id == evidence_id))
        if rec is None:
            raise HTTPException(status_code=404, detail="evidence record not found")
        return service._evidence_to_dict(rec)


@router.delete("/{evidence_id}", status_code=204)
def delete_evidence(
    evidence_id: str,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> None:
    with service.SessionLocal() as session:
        rec = session.scalar(select(EvidenceRecord).where(EvidenceRecord.evidence_id == evidence_id))
        if rec is None:
            raise HTTPException(status_code=404, detail="evidence record not found")
        session.delete(rec)
        session.commit()
    return None
