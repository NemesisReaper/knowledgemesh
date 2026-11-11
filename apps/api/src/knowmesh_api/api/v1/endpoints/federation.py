"""HTTP federation protocol, peer management, remote bundle retrieval, and pull-sync endpoints."""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from knowmesh_knowledge.models import PeerConnection

from knowmesh_api.dependencies import PrincipalContext, get_optional_principal, get_service, require_permission
from knowmesh_api.schemas import PeerRegisterRequest
from knowmesh_api.service import KnowMeshService

router = APIRouter()


@router.get("/identity")
def get_local_federation_identity(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.get_node_public_identity()


@router.get("/protocol/manifest")
@router.get("/manifest")
def get_federation_protocol_manifest(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    ident = service.get_node_public_identity()
    return {
        "protocol": "kyro-fed/1.0",
        "format": "OKF-v0.2",
        "signing_suite": "Ed25519",
        "canonicalization": "RFC-8785-JCS",
        "node_id": ident["node_id"],
        "name": ident["name"],
        "endpoint": ident["endpoint"],
        "capabilities": ident["capabilities"],
        "fingerprint": ident["key_fingerprint"],
        "features": [
            "independent-nodes",
            "ed25519-signatures",
            "rfc8785-jcs-digests",
            "pull-sync",
            "bm25-federated-search",
            "epistemic-separation",
        ],
    }


@router.get("/capabilities")
def get_local_federation_capabilities(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    ident = service.get_node_public_identity()
    return {
        "node_id": ident["node_id"],
        "name": ident["name"],
        "endpoint": ident["endpoint"],
        "capabilities": ident["capabilities"],
        "protocol_version": "1.0",
    }


@router.get("/health")
def get_local_federation_health(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    report = service.health_registry.run().to_dict()
    return {
        "node_id": service.settings.node_id,
        "status": report["status"],
        "checks": report["checks"],
    }


@router.get("/catalog")
def get_federation_catalog(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    return service.get_federation_catalog()


@router.post("/discover")
def federated_peer_discover(
    body: dict[str, Any],
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    query = str(body.get("query") or "")
    if not query.strip():
        raise HTTPException(status_code=422, detail="query is required")
    limit = int(body.get("limit") or 10)
    return service.search(
        query,
        limit=limit,
        scope="local",
        visibility="federated",
        include_private=False,
    )


@router.get("/bundles/{bundle_id}")
def get_federated_bundle_for_peer(
    bundle_id: str,
    revision: str | None = None,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        bundle = service.get_bundle(bundle_id, revision=revision, include_private=True)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if bundle.get("visibility") != "federated":
        raise HTTPException(
            status_code=403,
            detail=f"Bundle {bundle_id} has visibility={bundle.get('visibility')!r} and is not exposed to federated peers",
        )
    return bundle


@router.get("")
@router.get("/peers")
def list_peers(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_peers()
    return {"items": items[offset : offset + limit], "limit": limit, "offset": offset, "total": len(items)}


@router.post("", status_code=201)
@router.post("/peers", status_code=201)
def register_peer(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("federation:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    req = PeerRegisterRequest.model_validate({
        "peer_node_id": body.get("peer_node_id") or body.get("id"),
        "name": body.get("name") or body.get("title") or "Federated Peer",
        "endpoint": body.get("endpoint") or "https://peer.knowmesh.org",
        "public_key": body.get("public_key") or "",
        "key_fingerprint": body.get("key_fingerprint") or "",
        "capabilities": body.get("capabilities") or ["knowledge:search", "federation:sync"],
        "trust_level": body.get("trust_level") or "standard",
        "auto_approve": bool(body.get("auto_approve", False)),
    })
    try:
        return service.register_peer(
            peer_node_id=req.peer_node_id,
            name=req.name,
            endpoint=req.endpoint,
            public_key=req.public_key,
            key_fingerprint=req.key_fingerprint,
            capabilities=req.capabilities,
            trust_level=req.trust_level,
            auto_approve=req.auto_approve,
            actor_id=principal.actor_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/peers/{peer_id}/verify")
def verify_peer_identity(
    peer_id: str,
    principal: PrincipalContext = Depends(require_permission("federation:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.verify_peer(peer_id, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/peers/{peer_id}/approve")
def approve_peer(
    peer_id: str,
    approved: bool = Query(True),
    principal: PrincipalContext = Depends(require_permission("federation:manage")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.approve_peer(peer_id, approved=approved, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/peers/{peer_id}/sync")
def synchronize_peer(
    peer_id: str,
    principal: PrincipalContext = Depends(require_permission("federation:retrieve")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    try:
        return service.synchronize_peer(peer_id, actor_id=principal.actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/retrieve")
def retrieve_remote_bundle(
    body: dict[str, Any],
    principal: PrincipalContext = Depends(require_permission("federation:retrieve")),
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    peer_id = str(body.get("peer_id") or body.get("peer_node_id") or "")
    bundle_id = str(body.get("bundle_id") or "")
    revision = body.get("revision")
    persist = bool(body.get("persist", True))
    if not peer_id or not bundle_id:
        raise HTTPException(status_code=422, detail="peer_id and bundle_id are required")
    try:
        return service.retrieve_remote_bundle(
            peer_id,
            bundle_id,
            revision=revision,
            persist=persist,
            actor_id=principal.actor_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/syncs")
def list_sync_records(
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    items = service.list_sync_records()
    return {"items": items, "total": len(items)}


@router.get("/{peer_id}")
def get_peer(
    peer_id: str,
    service: KnowMeshService = Depends(get_service),
) -> dict[str, Any]:
    with service.SessionLocal() as session:
        peer = session.scalar(
            select(PeerConnection).where(
                (PeerConnection.peer_id == peer_id) | (PeerConnection.peer_node_id == peer_id)
            )
        )
        if peer is None:
            raise HTTPException(status_code=404, detail="federation record not found")
        return service._peer_to_dict(peer)


@router.delete("/{peer_id}", status_code=204)
def delete_peer(
    peer_id: str,
    principal: PrincipalContext = Depends(get_optional_principal),
    service: KnowMeshService = Depends(get_service),
) -> None:
    with service.SessionLocal() as session:
        peer = session.scalar(
            select(PeerConnection).where(
                (PeerConnection.peer_id == peer_id) | (PeerConnection.peer_node_id == peer_id)
            )
        )
        if peer is None:
            raise HTTPException(status_code=404, detail="federation record not found")
        session.delete(peer)
        session.commit()
    return None
