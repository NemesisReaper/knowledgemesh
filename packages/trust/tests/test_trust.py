import unittest

from packages.trust import (
    generate_keypair, sign_object, verify_artifact, VerificationStatus,
    RevocationRegistry, RevocationStatus, ProvenanceChain, ProvenanceAction,
    AccessControl, Principal, Resource, Permission, TrustPolicy, TrustLevel,
    evaluate_trust,
)


class TrustTests(unittest.TestCase):
    def setUp(self):
        self.keys = generate_keypair("node-a")
        self.artifact = {"id": "bundle-1", "claims": ["claim-1"]}
        self.signature = sign_object(self.artifact, self.keys)

    def test_signature_roundtrip_and_tamper(self):
        identities = {"node-a": self.keys.identity}
        good = verify_artifact(self.artifact, self.signature, identities)
        self.assertEqual(good.status, VerificationStatus.VERIFIED)
        bad = verify_artifact({"id": "bundle-1", "claims": ["changed"]},
                              self.signature, identities)
        self.assertFalse(bad.verified)

    def test_revocation(self):
        registry = RevocationRegistry()
        registry.revoke_subject("node-a", "key compromised", "admin")
        self.assertEqual(registry.status("node-a"), RevocationStatus.REVOKED)
        result = verify_artifact(self.artifact, self.signature,
                                 {"node-a": self.keys.identity},
                                 revoked_ids={"node-a"})
        self.assertEqual(result.status, VerificationStatus.REVOKED)

    def test_provenance_chain(self):
        chain = ProvenanceChain("bundle-1")
        chain.add(record_id="1", action=ProvenanceAction.CREATED, actor_id="node-a")
        chain.add(record_id="2", action=ProvenanceAction.REVIEWED, actor_id="reviewer")
        self.assertTrue(chain.verify())
        self.assertEqual(len(chain.records()), 2)

    def test_access_control_deny_by_default_and_grant(self):
        acl = AccessControl()
        principal = Principal("agent-1", frozenset({"reader"}))
        resource = Resource("bundle-1", owner_id="owner")
        self.assertFalse(acl.check(principal, resource, Permission.READ))
        acl.grant("reader", Permission.READ)
        self.assertTrue(acl.check(principal, resource, Permission.READ))

    def test_policy_evaluation(self):
        policy = TrustPolicy(require_signature=True, require_provenance=True)
        decision = evaluate_trust(
            policy, publisher_id="node-a", trust_level=TrustLevel.HIGH,
            signature_present=True, signature_valid=True, algorithm="Ed25519",
            provenance_valid=True, revoked=False,
        )
        self.assertTrue(decision.allowed)


if __name__ == "__main__":
    unittest.main()
