import pytest
from okf import (
    IssueSeverity,
    LinkRelation,
    OKFError,
    OKFLink,
    OKFResolver,
    calculate_canonical_hash,
    compute_merkle_root,
    parse_manifest,
    validate_manifest,
    verify_hash,
)


def test_canonical_hashing_and_merkle():
    h1 = calculate_canonical_hash({"b": 2, "a": 1})
    h2 = calculate_canonical_hash({"a": 1, "b": 2})
    assert h1 == h2
    assert verify_hash({"a": 1, "b": 2}, h1)
    root = compute_merkle_root([h1, h2])
    assert root.startswith("sha256:")


def test_parse_validate_and_resolve_manifest():
    raw = {
        "bundle_id": "demo-water-001",
        "title": "Water boiling point at standard pressure",
        "version": "1.0.0",
        "claims": [
            {
                "claim_id": "claim-water-001",
                "statement": "Pure water boils at approximately 100 C at 1 atm.",
                "evidence_ids": ["evidence-water-001"],
            }
        ],
        "evidence": [
            {
                "evidence_id": "evidence-water-001",
                "source_type": "reference",
                "description": "Primary thermodynamic table",
            }
        ],
        "links": [
            {
                "source": "evidence-water-001",
                "target": "claim-water-001",
                "relation": LinkRelation.SUPPORTS.value,
            }
        ],
    }
    manifest = parse_manifest(raw)
    report = validate_manifest(manifest)
    assert report.valid
    assert not report.errors

    resolver = OKFResolver([manifest])
    claim = resolver.resolve("okf://demo-water-001/claim-water-001")
    assert claim.claim_id == "claim-water-001"
    ev = resolver.resolve_claim_evidence("demo-water-001", "claim-water-001")
    assert len(ev) == 1 and ev[0].evidence_id == "evidence-water-001"


def test_validator_catches_dangling_references_and_tamper():
    raw = {
        "bundle_id": "bad-bundle",
        "title": "Broken",
        "claims": [
            {
                "claim_id": "c1",
                "statement": "Claim with missing evidence",
                "evidence_ids": ["missing-ev"],
            }
        ],
        "digest": "sha256:0000",
    }
    report = validate_manifest(raw)
    assert not report.valid
    codes = {issue.code for issue in report.errors}
    assert "dangling_evidence_reference" in codes
    assert "digest_mismatch" in codes

    with pytest.raises(OKFError):
        OKFLink(source="", target="c1")

