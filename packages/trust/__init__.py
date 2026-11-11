"""KnowMesh trust, identity, signature, provenance and access-control primitives."""

from .identity import (
    Identity, IdentityError, KeyPair, generate_keypair, identity_from_public_key,
    public_key_fingerprint,
)
from .signatures import (
    SignatureEnvelope, SignatureError, sign_bytes, sign_object,
    verify_bytes, verify_object,
)
from .verification import (
    VerificationResult, VerificationStatus, verify_artifact,
    verify_signature_envelope,
)
from .revocation import (
    RevocationRegistry, RevocationRecord, RevocationError, RevocationStatus,
)
from .provenance import (
    ProvenanceRecord, ProvenanceChain, ProvenanceError, ProvenanceAction,
)
from .access_control import (
    AccessControl, AccessDecision, AccessRequest, Permission, Principal,
    Resource, AccessControlError,
)
from .policies import (
    TrustPolicy, PolicyDecision, PolicyError, TrustLevel, evaluate_trust,
)

__all__ = [
    "Identity", "IdentityError", "KeyPair", "generate_keypair",
    "identity_from_public_key", "public_key_fingerprint",
    "SignatureEnvelope", "SignatureError", "sign_bytes", "sign_object",
    "verify_bytes", "verify_object", "VerificationResult",
    "VerificationStatus", "verify_artifact", "verify_signature_envelope",
    "RevocationRegistry", "RevocationRecord", "RevocationError",
    "RevocationStatus", "ProvenanceRecord", "ProvenanceChain",
    "ProvenanceError", "ProvenanceAction", "AccessControl",
    "AccessDecision", "AccessRequest", "Permission", "Principal",
    "Resource", "AccessControlError", "TrustPolicy", "PolicyDecision",
    "PolicyError", "TrustLevel", "evaluate_trust",
]
