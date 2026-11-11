"""Typed links between OKF knowledge artifacts and external URIs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .issues import OKFError


class LinkRelation(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    DERIVES_FROM = "derives_from"
    CITES = "cites"
    SUPERSEDES = "supersedes"
    RELATED_TO = "related_to"


@dataclass(frozen=True, slots=True)
class OKFLink:
    source: str
    target: str
    relation: LinkRelation = LinkRelation.RELATED_TO
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source or not self.source.strip():
            raise OKFError("link source is required")
        if not self.target or not self.target.strip():
            raise OKFError("link target is required")
        try:
            object.__setattr__(self, "relation", LinkRelation(self.relation))
        except ValueError as exc:
            raise OKFError(f"unsupported link relation: {self.relation}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation.value,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OKFLink":
        return cls(
            source=str(data.get("source", "")),
            target=str(data.get("target", "")),
            relation=LinkRelation(data.get("relation", LinkRelation.RELATED_TO.value)),
            metadata=dict(data.get("metadata") or {}),
        )


def parse_okf_uri(uri: str) -> tuple[str, str | None]:
    """Parse an OKF URI of the form 'okf://<bundle_id>' or 'okf://<bundle_id>/<item_id>'."""
    if not isinstance(uri, str) or not uri.startswith("okf://"):
        raise OKFError(f"invalid OKF URI: {uri!r}")
    rest = uri[len("okf://"):].strip("/")
    if not rest:
        raise OKFError("OKF URI must specify a bundle_id")
    parts = rest.split("/", 1)
    bundle_id = parts[0].strip()
    item_id = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
    if not bundle_id:
        raise OKFError("OKF URI bundle_id cannot be empty")
    return bundle_id, item_id

