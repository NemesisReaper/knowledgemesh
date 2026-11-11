"""Evaluation and winner selection for knowledge bounty submissions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .requests import BountyRequest
from .submissions import BountySubmission


@dataclass(frozen=True, slots=True)
class BountyEvaluation:
    submission_id: str
    bounty_id: str
    eligible: bool
    score: float
    reasons: tuple[str, ...] = ()


def evaluate_submission(
    bounty: BountyRequest,
    submission: BountySubmission,
    *,
    require_signature: bool = True,
) -> BountyEvaluation:
    """Evaluate a bounty submission against a bounty request's requirements."""
    reasons: list[str] = []
    if submission.bounty_id != bounty.bounty_id:
        reasons.append("submission bounty_id does not match bounty request")
    if not bounty.is_active():
        reasons.append("bounty is not active")
    if len(submission.evidence_ids) < bounty.minimum_evidence_count:
        reasons.append(
            f"insufficient evidence: {len(submission.evidence_ids)} < {bounty.minimum_evidence_count}"
        )
    if not submission.claim_ids:
        reasons.append("submission must include at least one claim")
    if require_signature and not submission.signature_verified:
        reasons.append("cryptographic signature is not verified")

    eligible = len(reasons) == 0
    evidence_bonus = min(1.0, len(submission.evidence_ids) / max(1, bounty.minimum_evidence_count))
    sig_bonus = 1.0 if submission.signature_verified else 0.5
    raw_score = (0.5 * submission.confidence + 0.3 * evidence_bonus + 0.2 * sig_bonus) if eligible else 0.0
    return BountyEvaluation(
        submission_id=submission.submission_id,
        bounty_id=bounty.bounty_id,
        eligible=eligible,
        score=round(raw_score, 6),
        reasons=tuple(reasons),
    )


def select_winning_submission(
    bounty: BountyRequest,
    submissions: Iterable[BountySubmission],
    *,
    require_signature: bool = True,
) -> BountyEvaluation | None:
    """Return the highest-scoring eligible submission evaluation, or None if none qualify."""
    evaluations = [
        evaluate_submission(bounty, sub, require_signature=require_signature)
        for sub in submissions
    ]
    eligible = [ev for ev in evaluations if ev.eligible]
    if not eligible:
        return None
    eligible.sort(key=lambda ev: (-ev.score, ev.submission_id))
    return eligible[0]

