from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Mapping, Sequence

@dataclass(frozen=True)
class MergeConflict:
    path: tuple[str, ...]
    values: tuple[Any, ...]

@dataclass(frozen=True)
class MergeResult:
    payload: dict[str, Any] | None
    source_ids: tuple[str, ...]
    conflicts: tuple[MergeConflict, ...]
    @property
    def successful(self) -> bool: return self.payload is not None and not self.conflicts

def merge_knowledge(sources: Mapping[str, Mapping[str, Any]], *,
                    conflict_policy: str = "error",
                    list_policy: str = "replace") -> MergeResult:
    """Merge mappings recursively; never silently resolve conflicting scalar values.

    conflict_policy: 'error', 'first', or 'last'. list_policy: 'replace' or 'union'.
    """
    if len(sources) < 2: raise ValueError("merge requires at least two sources")
    if conflict_policy not in {"error", "first", "last"}: raise ValueError("invalid conflict_policy")
    if list_policy not in {"replace", "union"}: raise ValueError("invalid list_policy")
    ids = tuple(sources.keys())
    conflicts: list[MergeConflict] = []
    result = deepcopy(dict(sources[ids[0]]))
    def combine(dst, src, path=()):
        for key, value in src.items():
            p = path + (str(key),)
            if key not in dst:
                dst[key] = deepcopy(value); continue
            old = dst[key]
            if isinstance(old, dict) and isinstance(value, Mapping):
                combine(old, value, p)
            elif old == value:
                continue
            elif isinstance(old, list) and isinstance(value, list) and list_policy == "union":
                for item in value:
                    if item not in old: old.append(deepcopy(item))
            else:
                conflicts.append(MergeConflict(p, (deepcopy(old), deepcopy(value))))
                if conflict_policy == "last": dst[key] = deepcopy(value)
    for sid in ids[1:]: combine(result, sources[sid])
    if conflicts and conflict_policy == "error": return MergeResult(None, ids, tuple(conflicts))
    result["_lineage"] = {"relation": "merged_from", "source_ids": list(ids)}
    return MergeResult(result, ids, tuple(conflicts))
