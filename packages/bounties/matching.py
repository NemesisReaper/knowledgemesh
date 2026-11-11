"""Candidate matching for knowledge bounties based on capabilities, domain, and reputation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .requests import BountyRequest


@dataclass(frozen=True, slots=True)
class CandidateProfile:
    node_id: str
    domains: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    reputation: float = 0.5
    available: bool = True

    def __post_init__(self) -> None:
        if not self.node_id or not self.node_id.strip():
            raise ValueError("node_id is required")
        if not 0.0 <= self.reputation <= 1.0:
            raise ValueError("reputation must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class BountyMatch:
    bounty_id: str
    node_id: str
    score: float
    matched_capabilities: tuple[str, ...]
    domain_match: bool


def match_bounty_candidates(
    bounty: BountyRequest,
    candidates: Iterable[CandidateProfile],
    *,
    limit: int = 10,
) -> tuple[BountyMatch, ...]:
    """Rank eligible candidate nodes for a bounty request."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    required_caps = set(bounty.required_capabilities)
    matches: list[BountyMatch] = []
    for candidate in candidates:
        if not candidate.available:
            continue
        if candidate.reputation < bounty.minimum_reputation:
            continue
        cand_caps = set(candidate.capabilities)
        if not required_caps.issubset(cand_caps):
            continue
        domain_match = bounty.domain in candidate.domains or "*" in candidate.domains
        cap_overlap = tuple(sorted(required_caps & cand_caps))
        score = (0.6 * candidate.reputation) + (0.4 if domain_match else 0.1)
        matches.append(
            BountyMatch(
                bounty_id=bounty.bounty_id,
                node_id=candidate.node_id,
                score=round(score, 6),
                matched_capabilities=cap_overlap,
                domain_match=domain_match,
            )
        )
    matches.sort(key=lambda m: (-m.score, m.node_id))
    return tuple(matches[:limit])

