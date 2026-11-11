from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Mapping

class SyncState(str, Enum):
    NEW="new"
    PLANNED="planned"
    IN_PROGRESS="in_progress"
    SUCCEEDED="succeeded"
    PARTIAL="partial"
    FAILED="failed"
    CONFLICT="conflict"

@dataclass(frozen=True)
class SyncItem:
    artifact_id: str
    local_fingerprint: str | None
    remote_fingerprint: str | None
    action: str
    def __post_init__(self):
        if not self.artifact_id: raise ValueError("artifact_id required")
        if self.action not in {"push","pull","unchanged","conflict"}:
            raise ValueError("unsupported sync action")

@dataclass(frozen=True)
class SyncPlan:
    sync_id: str
    source_peer_id: str
    target_peer_id: str
    items: tuple[SyncItem,...]
    state: SyncState = SyncState.PLANNED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Mapping[str,object] = field(default_factory=dict)
    def __post_init__(self):
        if not self.sync_id or not self.source_peer_id or not self.target_peer_id:
            raise ValueError("sync_id and peer IDs are required")
        if self.source_peer_id == self.target_peer_id:
            raise ValueError("source and target peers must differ")
        if self.created_at.tzinfo is None: raise ValueError("created_at must be timezone-aware")

def plan_sync(sync_id: str, source_peer_id: str, target_peer_id: str,
              source_manifest: Mapping[str,str],
              target_manifest: Mapping[str,str]) -> SyncPlan:
    """Build a deterministic push/pull/no-op/conflict plan from artifact fingerprints.

    Conflict means both sides have diverged from a known common base; callers should
    supply base_fingerprints to distinguish that case from a one-way update.
    This simple planner treats unequal existing fingerprints as conflict.
    """
    items=[]
    for artifact_id in sorted(set(source_manifest)|set(target_manifest)):
        source=source_manifest.get(artifact_id); target=target_manifest.get(artifact_id)
        if source is None: action="pull"
        elif target is None: action="push"
        elif source == target: action="unchanged"
        else: action="conflict"
        items.append(SyncItem(artifact_id,source,target,action))
    return SyncPlan(sync_id,source_peer_id,target_peer_id,tuple(items))

def apply_sync_receipt(plan: SyncPlan, outcomes: Mapping[str,str]) -> SyncPlan:
    """Return an updated plan from per-artifact outcomes; does not copy artifact data."""
    expected={item.artifact_id for item in plan.items if item.action in {"push","pull"}}
    if set(outcomes)-expected: raise ValueError("receipt contains unknown or non-transfer artifact IDs")
    if any(v not in {"success","failed","conflict"} for v in outcomes.values()):
        raise ValueError("outcomes must be success, failed, or conflict")
    if not expected:
        state=SyncState.CONFLICT if any(i.action=="conflict" for i in plan.items) else SyncState.SUCCEEDED
    elif set(outcomes) != expected:
        state=SyncState.PARTIAL if outcomes else SyncState.PLANNED
    elif all(v=="success" for v in outcomes.values()):
        state=SyncState.SUCCEEDED
    elif any(v=="conflict" for v in outcomes.values()):
        state=SyncState.CONFLICT
    elif any(v=="success" for v in outcomes.values()):
        state=SyncState.PARTIAL
    else: state=SyncState.FAILED
    return SyncPlan(plan.sync_id,plan.source_peer_id,plan.target_peer_id,
                    plan.items,state,plan.created_at,plan.metadata)
