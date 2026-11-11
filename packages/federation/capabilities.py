from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, Mapping

@dataclass(frozen=True)
class Capability:
    name: str
    version: str = "1"
    parameters: Mapping[str, object] = field(default_factory=dict)
    def __post_init__(self):
        if not self.name.strip(): raise ValueError("capability name is required")
        if not self.version.strip(): raise ValueError("capability version is required")

@dataclass(frozen=True)
class CapabilitySet:
    capabilities: tuple[Capability, ...] = ()

    @classmethod
    def from_names(cls, names: Iterable[str]) -> "CapabilitySet":
        return cls(tuple(Capability(n) for n in sorted(set(names))))

    def names(self) -> frozenset[str]:
        return frozenset(c.name for c in self.capabilities)

    def supports(self, required: Iterable[str]) -> bool:
        return set(required).issubset(self.names())

    def missing(self, required: Iterable[str]) -> tuple[str, ...]:
        return tuple(sorted(set(required) - self.names()))

    def intersect(self, other: "CapabilitySet") -> "CapabilitySet":
        right = {c.name: c for c in other.capabilities}
        return CapabilitySet(tuple(c for c in self.capabilities if c.name in right
                                   and c.version == right[c.name].version))
