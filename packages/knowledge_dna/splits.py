from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Mapping, Sequence

@dataclass(frozen=True)
class SplitResult:
    parent_id: str
    children: dict[str, dict[str, Any]]
    partition_key: str

def split_knowledge(parent_id: str, payload: Mapping[str, Any], *,
                    partition_key: str, partitions: Mapping[str, Sequence[Any]]) -> SplitResult:
    """Create child payloads by partitioning one list-valued field.

    The parent is not modified. Each child receives a deep copy of all other fields.
    """
    if not parent_id or not partition_key: raise ValueError("parent_id and partition_key are required")
    source = payload.get(partition_key)
    if not isinstance(source, list): raise TypeError("partition_key must identify a list")
    if not partitions: raise ValueError("at least one partition is required")
    flattened = [item for values in partitions.values() for item in values]
    if len(flattened) != len(set(_freeze(x) for x in flattened)):
        raise ValueError("partition values must not overlap")
    source_frozen = {_freeze(x) for x in source}
    if any(_freeze(x) not in source_frozen for x in flattened):
        raise ValueError("partition contains values not present in parent")
    children = {}
    for child_id, values in partitions.items():
        if not child_id or child_id == parent_id: raise ValueError("invalid child id")
        child = deepcopy(dict(payload))
        child[partition_key] = [deepcopy(x) for x in values]
        child["_lineage"] = {"relation": "split_from", "parent_id": parent_id}
        children[child_id] = child
    return SplitResult(parent_id, children, partition_key)

def _freeze(value):
    if isinstance(value, dict): return tuple(sorted((k, _freeze(v)) for k,v in value.items()))
    if isinstance(value, list): return tuple(_freeze(v) for v in value)
    if isinstance(value, set): return tuple(sorted(_freeze(v) for v in value))
    try: hash(value); return value
    except TypeError: return repr(value)
