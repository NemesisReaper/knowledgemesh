"""Atomic claims lifecycle and evaluation endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query

from core import new_id
from knowmesh_knowledge.models import ClaimRecord
from sqlalchemy import select

from knowmesh_api.dependencies import PrincipalContext, get_optional_principal, get_service, require_permission
from knowmesh_api.schemas import ClaimStatusUpdateRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.get("")
def list_claims(
    bundle_id: str | None = None,
    status: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_claims(bundle_id=bundle_id, status=status)
    if q:
        ql = q.casefold()
        items = [i for i in items if ql in str(i).casefold()]
    return {"items": items[offset : offset + limit], "limit": limit, "offset": offset, "total": len(items)}


@router.post("", status_code=201)
def create_claim(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("knowledge:publish")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    cid = str(body.get("claim_id") or body.get("id") or new_id("claim"))
    stmt = str(body.get("statement") or body.get("title") or body.get("content") or "Untitled Claim")
    bundle_id = str(body.get("bundle_id") or "standalone-bundle")
    ev_ids = list(body.get("evidence_ids") or [])
    status_val = str(body.get("status") or ("evidence_attached" if ev_ids else "proposed"))
    with service.SessionLocal() as session:
        existing = session.scalar(select(ClaimRecord).where(ClaimRecord.claim_id == cid))
        if existing is not None:
            existing.statement = stmt
            existing.status = status_val
            rec = existing
        else:
            rec = ClaimRecord(
                claim_id=cid,
                bundle_id=bundle_id,
                revision=str(body.get("revision") or "1.0.0"),
                statement=stmt,
                claim_type=str(body.get("claim_type") or "factual"),
                domain=str(body.get("domain") or "general"),
                subject=body.get("subject"),
                predicate=body.get("predicate"),
                object_val=body.get("object"),
                status=status_val,
                supporting_evidence_ids_json=ev_ids,
                contradictory_evidence_ids_json=list(body.get("contradictory_evidence_ids") or []),
                source_references_json=list(body.get("source_references") or []),
                metadata_json=dict(body.get("metadata") or body.get("payload") or {}),
            )
            session.add(rec)
        session.commit()
        return service._claim_to_dict(rec)


@router.get("/{claim_id}")
def get_claim(
    claim_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    with service.SessionLocal() as session:
        rec = session.scalar(select(ClaimRecord).where(ClaimRecord.claim_id == claim_id))
        if rec is None:
            raise HTTPException(status_code=404, detail="claims record not found")
        return service._claim_to_dict(rec)


@router.patch("/{claim_id}/status")
@router.post("/{claim_id}/evaluate")
def update_or_evaluate_claim(
    claim_id: str,
    body: ClaimStatusUpdateRequest | None = None,
    principal: PrincipalContext = Depends(require_permission("knowledge:update")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.evaluate_and_update_claim(
            claim_id,
            new_status=body.status if body else None,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/{claim_id}", status_code=204)
def delete_claim(
    claim_id: str,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> None:
    with service.SessionLocal() as session:
        rec = session.scalar(select(ClaimRecord).where(ClaimRecord.claim_id == claim_id))
        if rec is None:
            raise HTTPException(status_code=404, detail="claims record not found")
        session.delete(rec)
        session.commit()
    return None
