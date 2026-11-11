"""Authentication, password hashing, token signing, credential hashing, RBAC, and SSRF protection."""

from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import ipaddress
import json
import secrets
from threading import RLock
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse


ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "owner": frozenset({
        "org:manage",
        "organization:manage",
        "org:read",
        "member:manage",
        "node:manage",
        "node:read",
        "agent:manage",
        "agent:read",
        "credential:manage",
        "knowledge:read",
        "knowledge:search",
        "knowledge:publish",
        "knowledge:update",
        "federation:manage",
        "federation:discover",
        "federation:retrieve",
        "verification:read",
        "trust:manage",
        "audit:read",
    }),
    "administrator": frozenset({
        "org:manage",
        "organization:manage",
        "org:read",
        "member:manage",
        "node:manage",
        "node:read",
        "agent:manage",
        "agent:read",
        "credential:manage",
        "knowledge:read",
        "knowledge:search",
        "knowledge:publish",
        "knowledge:update",
        "federation:manage",
        "federation:discover",
        "federation:retrieve",
        "verification:read",
        "trust:manage",
        "audit:read",
    }),
    "curator": frozenset({
        "org:read",
        "node:read",
        "agent:read",
        "knowledge:read",
        "knowledge:search",
        "knowledge:publish",
        "knowledge:update",
        "federation:discover",
        "federation:retrieve",
        "verification:read",
        "audit:read",
    }),
    "developer": frozenset({
        "org:read",
        "node:read",
        "agent:manage",
        "agent:read",
        "knowledge:read",
        "knowledge:search",
        "federation:discover",
        "federation:retrieve",
        "verification:read",
    }),
    "member": frozenset({
        "org:read",
        "node:read",
        "agent:read",
        "knowledge:read",
        "knowledge:search",
        "federation:discover",
        "verification:read",
    }),
}

VALID_AGENT_PERMISSIONS: frozenset[str] = frozenset({
    "knowledge:read",
    "knowledge:search",
    "knowledge:publish",
    "knowledge:update",
    "federation:discover",
    "federation:retrieve",
    "verification:read",
})

DEFAULT_AGENT_PERMISSIONS: tuple[str, ...] = (
    "knowledge:read",
    "knowledge:search",
    "verification:read",
)


def hash_password(password: str) -> str:
    """Hash a password using scrypt with a random 16-byte salt."""
    if not isinstance(password, str) or len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=32,
    )
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    dk_b64 = base64.urlsafe_b64encode(derived).decode("ascii").rstrip("=")
    return f"scrypt$16384$8$1${salt_b64}${dk_b64}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored scrypt hash in constant time."""
    if not password or not stored_hash:
        return False
    try:
        parts = stored_hash.split("$")
        if len(parts) != 6 or parts[0] != "scrypt":
            return False
        n, r, p = int(parts[1]), int(parts[2]), int(parts[3])
        salt = base64.urlsafe_b64decode(parts[4] + "=" * (-len(parts[4]) % 4))
        expected = base64.urlsafe_b64decode(parts[5] + "=" * (-len(parts[5]) % 4))
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            dklen=len(expected),
        )
        return hmac.compare_digest(derived, expected)
    except Exception:
        return False


def generate_api_credential() -> tuple[str, str, str]:
    """Generate a one-time API credential secret, its prefix, and its SHA-256 hash."""
    raw_token = f"km_live_{secrets.token_urlsafe(24)}"
    prefix = raw_token[:14]
    secret_hash = hash_credential_secret(raw_token)
    return raw_token, prefix, secret_hash


def hash_credential_secret(raw_secret: str) -> str:
    return hashlib.sha256(raw_secret.encode("utf-8")).hexdigest()


class TokenRevocationStore:
    """Thread-safe revocation store for JWT/HMAC session tokens."""

    def __init__(self) -> None:
        self._revoked_jtis: set[str] = set()
        self._lock = RLock()

    def revoke(self, jti: str) -> None:
        with self._lock:
            self._revoked_jtis.add(jti)

    def is_revoked(self, jti: str) -> bool:
        with self._lock:
            return jti in self._revoked_jtis


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_signed_token(
    subject_id: str,
    *,
    secret_key: str,
    ttl_seconds: int = 3600,
    token_type: str = "access",
    organization_id: str | None = None,
    role: str = "owner",
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=ttl_seconds)
    jti = secrets.token_hex(12)
    payload: dict[str, Any] = {
        "sub": subject_id,
        "jti": jti,
        "type": token_type,
        "org_id": organization_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    if extra:
        payload.update(extra)
    header_bytes = json.dumps({"alg": "HS256", "typ": "KM-JWT"}, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    signing_input = f"{_b64encode(header_bytes)}.{_b64encode(payload_bytes)}".encode("ascii")
    sig = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    token = f"{signing_input.decode('ascii')}.{_b64encode(sig)}"
    return {
        "token": token,
        "jti": jti,
        "expires_at": exp.isoformat(),
        "payload": payload,
    }


def verify_signed_token(
    token: str,
    *,
    secret_key: str,
    expected_type: str | None = None,
    revocation_store: TokenRevocationStore | None = None,
) -> dict[str, Any]:
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token")
        signing_input = f"{parts[0]}.{parts[1]}".encode("ascii")
        expected_sig = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
        actual_sig = _b64decode(parts[2])
        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid token signature")
        payload = json.loads(_b64decode(parts[1]).decode("utf-8"))
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Invalid token encoding") from exc

    now_ts = int(datetime.now(timezone.utc).timestamp())
    if int(payload.get("exp", 0)) < now_ts:
        raise ValueError("Token has expired")
    if expected_type and payload.get("type") != expected_type:
        raise ValueError(f"Expected {expected_type} token")
    if revocation_store and revocation_store.is_revoked(str(payload.get("jti", ""))):
        raise ValueError("Token has been revoked")
    return payload


def validate_agent_permissions(permissions: Iterable[str]) -> list[str]:
    result = []
    for perm in permissions:
        p = str(perm).strip()
        if p not in VALID_AGENT_PERMISSIONS:
            raise ValueError(f"Unsupported agent permission: {p!r}")
        if p not in result:
            result.append(p)
    return result


def validate_peer_endpoint(endpoint: str, *, allow_local: bool = True) -> str:
    """Validate peer HTTP endpoint and guard against SSRF targets."""
    if not endpoint or not isinstance(endpoint, str):
        raise ValueError("Peer endpoint is required")
    cleaned = endpoint.strip().rstrip("/")
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Peer endpoint must use http or https scheme")
    if not parsed.hostname:
        raise ValueError("Peer endpoint must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("Peer endpoint must not contain embedded credentials")

    host = parsed.hostname.lower()
    blocked_hosts = {"169.254.169.254", "metadata.google.internal", "0.0.0.0"}
    if host in blocked_hosts:
        raise ValueError(f"Peer endpoint host {host!r} is blocked by SSRF policy")

    try:
        ip = ipaddress.ip_address(host)
        if ip.is_link_local or ip.is_multicast or ip.is_unspecified:
            raise ValueError(f"Peer IP {host} is not permitted by SSRF policy")
        if not allow_local and (ip.is_loopback or ip.is_private):
            raise ValueError(f"Private/loopback peer IP {host} is not permitted in this environment")
    except ValueError as exc:
        if "SSRF" in str(exc) or "permitted" in str(exc):
            raise

    return cleaned
