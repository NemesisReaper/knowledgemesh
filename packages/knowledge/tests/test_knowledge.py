from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, configure_mappers

from knowmesh_knowledge.models import (
    Base,
    Bundle,
    BundleVersion,
    Claim,
    ClaimEvidence,
    Evidence,
    Lineage,
    NetworkNode,
    Operation,
    PublisherIdentity,
    Verification,
)


def test_models_roundtrip_and_relationships():
    configure_mappers()
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        node = NetworkNode(node_id="node-a", endpoint="https://node-a.example")
        session.add(node)
        session.flush()

        identity = PublisherIdentity(
            node_id=node.id,
            public_key="pub-key-1",
            key_fingerprint="fp-1",
        )
        session.add(identity)
        session.flush()

        node.identity_id = identity.id
        bundle = Bundle(
            publisher_id=identity.id,
            bundle_identifier="bundle-water-001",
            title="Water boiling point",
        )
        session.add(bundle)
        session.flush()

        version = BundleVersion(
            bundle_id=bundle.id,
            version="1.0.0",
            digest="sha256:abc",
            manifest={"claims": 1},
        )
        session.add(version)
        session.flush()

        claim = Claim(
            bundle_version_id=version.id,
            statement="Pure water boils at 100 C at 1 atm.",
            domain="physics",
        )
        evidence = Evidence(
            source_uri="https://example.org/ref",
            content_hash="sha256:def",
            evidence_type="reference",
        )
        session.add_all([claim, evidence])
        session.flush()

        link = ClaimEvidence(
            claim_id=claim.id,
            evidence_id=evidence.id,
            relationship="supports",
        )
        verification = Verification(
            claim_id=claim.id,
            verifier_id=identity.id,
            outcome="verified",
            confidence=0.95,
            signature="sig-123",
        )
        lineage = Lineage(
            parent_bundle_id=None,
            child_bundle_id=bundle.id,
            operation="created",
            actor_id=identity.id,
        )
        op = Operation(
            operation_type="publish",
            entity_type="bundle",
            entity_id=bundle.id,
            actor_id=identity.id,
        )
        session.add_all([link, verification, lineage, op])
        session.commit()

        loaded_ver = session.scalar(select(Verification))
        assert loaded_ver is not None
        assert loaded_ver.verifier.key_fingerprint == "fp-1"
        assert loaded_ver.claim.domain == "physics"

    Base.metadata.drop_all(engine)

