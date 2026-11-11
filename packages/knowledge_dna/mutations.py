from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy
from typing import Any, Mapping

class MutationKind(str, Enum):
    SET = "set"
    REMOVE = "remove"
    APPEND = "append"
    INCREMENT = "increment"
    MERGE = "merge"

@dataclass(frozen=True)
class Mutation:
    kind: MutationKind
    path: tuple[str, ...]
    value: Any = None
    reason: str = ""
    actor: str = "unknown"

    def __post_init__(self):
        if not self.path or any(not isinstance(p, str) or not p for p in self.path):
            raise ValueError("path must contain non-empty string keys")
        if self.kind in (MutationKind.SET, MutationKind.APPEND, MutationKind.INCREMENT, MutationKind.MERGE) and self.value is None:
            raise ValueError(f"{self.kind.value} requires a value")

@dataclass(frozen=True)
class MutationResult:
    payload: dict[str, Any]
    changed: bool
    operation: Mutation
    before_value: Any
    after_value: Any

def _parent(doc: dict[str, Any], path: tuple[str, ...], create: bool):
    cur = doc
    for key in path[:-1]:
        if key not in cur:
            if not create: raise KeyError(".".join(path))
            cur[key] = {}
        if not isinstance(cur[key], dict): raise TypeError(f"{key!r} is not an object")
        cur = cur[key]
    return cur, path[-1]

def apply_mutation(payload: Mapping[str, Any], mutation: Mutation) -> MutationResult:
    """Apply one explicit, deterministic mutation to a JSON-like mapping."""
    doc = deepcopy(dict(payload))
    parent, key = _parent(doc, mutation.path, mutation.kind in (MutationKind.SET, MutationKind.MERGE))
    before = deepcopy(parent.get(key))
    if mutation.kind == MutationKind.SET:
        parent[key] = deepcopy(mutation.value)
    elif mutation.kind == MutationKind.REMOVE:
        if key not in parent: raise KeyError(".".join(mutation.path))
        del parent[key]
    elif mutation.kind == MutationKind.APPEND:
        if key not in parent: parent[key] = []
        if not isinstance(parent[key], list): raise TypeError("append target must be a list")
        parent[key].append(deepcopy(mutation.value))
    elif mutation.kind == MutationKind.INCREMENT:
        if key not in parent: parent[key] = 0
        if isinstance(parent[key], bool) or not isinstance(parent[key], (int, float)):
            raise TypeError("increment target must be numeric")
        if isinstance(mutation.value, bool) or not isinstance(mutation.value, (int, float)):
            raise TypeError("increment value must be numeric")
        parent[key] += mutation.value
    elif mutation.kind == MutationKind.MERGE:
        if key not in parent: parent[key] = {}
        if not isinstance(parent[key], dict) or not isinstance(mutation.value, Mapping):
            raise TypeError("merge target and value must be objects")
        parent[key].update(deepcopy(dict(mutation.value)))
    after = deepcopy(parent.get(key))
    return MutationResult(doc, before != after, mutation, before, after)
