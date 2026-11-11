import pytest
from bounties import (
    BountyError,
    BountyRequest,
    BountySubmission,
    CandidateProfile,
    evaluate_submission,
    match_bounty_candidates,
    select_winning_submission,
)


def test_bounty_matching_and_evaluation():
    bounty = BountyRequest(
        bounty_id="b-1",
        title="Verify LLM context window degradation claim",
        domain="ai-safety",
        requester_id="node-a",
        required_capabilities=("verify", "benchmark"),
        minimum_reputation=0.6,
        minimum_evidence_count=2,
    )
    candidates = [
        CandidateProfile("node-b", domains=("ai-safety",), capabilities=("verify", "benchmark"), reputation=0.85),
        CandidateProfile("node-c", domains=("physics",), capabilities=("verify", "benchmark"), reputation=0.70),
        CandidateProfile("node-d", domains=("ai-safety",), capabilities=("verify",), reputation=0.95),
    ]
    matches = match_bounty_candidates(bounty, candidates)
    assert [m.node_id for m in matches] == ["node-b", "node-c"]
    assert matches[0].domain_match is True

    sub_bad = BountySubmission(
        submission_id="sub-1",
        bounty_id="b-1",
        contributor_id="node-c",
        bundle_id="bun-1",
        claim_ids=("c1",),
        evidence_ids=("e1",),
        signature_verified=True,
    )
    sub_good = BountySubmission(
        submission_id="sub-2",
        bounty_id="b-1",
        contributor_id="node-b",
        bundle_id="bun-2",
        claim_ids=("c1",),
        evidence_ids=("e1", "e2"),
        confidence=0.9,
        signature_verified=True,
    )
    eval_bad = evaluate_submission(bounty, sub_bad)
    assert not eval_bad.eligible
    winner = select_winning_submission(bounty, [sub_bad, sub_good])
    assert winner is not None
    assert winner.submission_id == "sub-2"

    with pytest.raises(BountyError):
        BountyRequest(bounty_id="", title="x", domain="d", requester_id="r")

