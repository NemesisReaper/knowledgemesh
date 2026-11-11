"""Structural and referential integrity validator for OKF manifests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .issues import IssueSeverity, OKFError, OKFIssue
from .manifest import OKFManifest, SUPPORTED_FORMAT_VERSIONS
from .parser import parse_manifest


@dataclass(frozen=True, slots=True)
class ValidationReport:
    valid: bool
    issues: tuple[OKFIssue, ...]

    @property
    def errors(self) -> tuple[OKFIssue, ...]:
        return tuple(i for i in self.issues if i.severity == IssueSeverity.ERROR)

    @property
    def warnings(self) -> tuple[OKFIssue, ...]:
        return tuple(i for i in self.issues if i.severity == IssueSeverity.WARNING)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "issues": [i.to_dict() for i in self.issues],
        }


def validate_manifest(source: OKFManifest | Mapping[str, Any]) -> ValidationReport:
    """Validate an OKFManifest or raw dictionary and return a ValidationReport."""
    issues: list[OKFIssue] = []
    if not isinstance(source, OKFManifest):
        try:
            manifest = parse_manifest(source)
        except OKFError as exc:
            return ValidationReport(
                valid=False,
                issues=(OKFIssue("parse_error", str(exc), IssueSeverity.ERROR),),
            )
    else:
        manifest = source

    if manifest.format_version not in SUPPORTED_FORMAT_VERSIONS:
        issues.append(
            OKFIssue(
                "unsupported_format_version",
                f"Format version {manifest.format_version!r} is not in {sorted(SUPPORTED_FORMAT_VERSIONS)}",
                IssueSeverity.ERROR,
                path="format_version",
            )
        )

    expected_digest = manifest.compute_digest()
    if manifest.digest and manifest.digest != expected_digest:
        issues.append(
            OKFIssue(
                "digest_mismatch",
                f"Manifest digest {manifest.digest} does not match computed digest {expected_digest}",
                IssueSeverity.ERROR,
                path="digest",
            )
        )

    expected_merkle = manifest.compute_merkle_root()
    if manifest.merkle_root and manifest.merkle_root != expected_merkle:
        issues.append(
            OKFIssue(
                "merkle_root_mismatch",
                "Manifest merkle_root does not match computed Merkle root",
                IssueSeverity.ERROR,
                path="merkle_root",
            )
        )

    claim_ids: set[str] = set()
    for idx, claim in enumerate(manifest.claims):
        if claim.claim_id in claim_ids:
            issues.append(
                OKFIssue(
                    "duplicate_claim_id",
                    f"Duplicate claim_id: {claim.claim_id}",
                    IssueSeverity.ERROR,
                    path=f"claims[{idx}].claim_id",
                )
            )
        claim_ids.add(claim.claim_id)
        if not claim.evidence_ids:
            issues.append(
                OKFIssue(
                    "ungrounded_claim",
                    f"Claim {claim.claim_id} has no linked evidence_ids",
                    IssueSeverity.WARNING,
                    path=f"claims[{idx}].evidence_ids",
                )
            )

    evidence_ids: set[str] = set()
    for idx, ev in enumerate(manifest.evidence):
        if ev.evidence_id in evidence_ids:
            issues.append(
                OKFIssue(
                    "duplicate_evidence_id",
                    f"Duplicate evidence_id: {ev.evidence_id}",
                    IssueSeverity.ERROR,
                    path=f"evidence[{idx}].evidence_id",
                )
            )
        evidence_ids.add(ev.evidence_id)

    for idx, claim in enumerate(manifest.claims):
        for eid in claim.evidence_ids:
            if eid not in evidence_ids:
                issues.append(
                    OKFIssue(
                        "dangling_evidence_reference",
                        f"Claim {claim.claim_id} references unknown evidence_id {eid}",
                        IssueSeverity.ERROR,
                        path=f"claims[{idx}].evidence_ids",
                    )
                )

    known_targets = claim_ids | evidence_ids | {manifest.bundle_id}
    for idx, link in enumerate(manifest.links):
        if link.source not in known_targets and not link.source.startswith(("okf://", "http://", "https://")):
            issues.append(
                OKFIssue(
                    "unknown_link_source",
                    f"Link source {link.source!r} is not a local artifact ID or URI",
                    IssueSeverity.ERROR,
                    path=f"links[{idx}].source",
                )
            )
        if link.target not in known_targets and not link.target.startswith(("okf://", "http://", "https://")):
            issues.append(
                OKFIssue(
                    "unknown_link_target",
                    f"Link target {link.target!r} is not a local artifact ID or URI",
                    IssueSeverity.ERROR,
                    path=f"links[{idx}].target",
                )
            )

    has_errors = any(i.severity == IssueSeverity.ERROR for i in issues)
    return ValidationReport(valid=not has_errors, issues=tuple(issues))

