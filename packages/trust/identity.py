"""Ed25519 identity and key management primitives.

Private keys are deliberately not serialized by Identity. Persist private
key bytes only in an appropriately protected secret store.
"""

from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
import secrets
from typing import Any


class IdentityError(ValueError):
    pass


# --- Pure-Python RFC 8032 Ed25519 fallback when 'cryptography' is unavailable ---
_P = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, _P - 2, _P)) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    x = pow(xx, (_P + 3) // 8, _P)
    if (x * x - xx) % _P != 0:
        x = (x * _I) % _P
    if x % 2 != 0:
        x = _P - x
    return x


_BY = 4 * pow(5, _P - 2, _P) % _P
_BX = _xrecover(_BY)
_B = (_BX % _P, _BY % _P, 1, (_BX * _BY) % _P)
_ZERO = (0, 1, 1, 0)


def _edwards_add(p1: tuple[int, int, int, int], p2: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    a = (y1 - x1) * (y2 - x2) % _P
    b = (y1 + x1) * (y2 + x2) % _P
    c = 2 * t1 * t2 * _D % _P
    d = 2 * z1 * z2 % _P
    e = (b - a) % _P
    f = (d - c) % _P
    g = (d + c) % _P
    h = (b + a) % _P
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _scalarmult(pt: tuple[int, int, int, int], e: int) -> tuple[int, int, int, int]:
    res = _ZERO
    cur = pt
    while e > 0:
        if e & 1:
            res = _edwards_add(res, cur)
        cur = _edwards_add(cur, cur)
        e >>= 1
    return res


def _encodepoint(pt: tuple[int, int, int, int]) -> bytes:
    x, y, z, _ = pt
    zi = pow(z, _P - 2, _P)
    x = (x * zi) % _P
    y = (y * zi) % _P
    val = y | ((x & 1) << 255)
    return val.to_bytes(32, "little")


def _decodepoint(s: bytes) -> tuple[int, int, int, int]:
    if len(s) != 32:
        raise ValueError("Invalid point length")
    unclamped = int.from_bytes(s, "little")
    y = unclamped & ((1 << 255) - 1)
    x_sign = (unclamped >> 255) & 1
    if y >= _P:
        raise ValueError("Point y out of range")
    xx = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    x = pow(xx, (_P + 3) // 8, _P)
    if (x * x - xx) % _P != 0:
        x = (x * _I) % _P
    if (x * x - xx) % _P != 0:
        raise ValueError("Point is not on curve")
    if x == 0 and x_sign == 1:
        raise ValueError("Invalid x sign for x=0")
    if (x & 1) != x_sign:
        x = _P - x
    return (x, y, 1, (x * y) % _P)


class _FallbackSerialization:
    class Encoding:
        Raw = "raw"

    class PrivateFormat:
        Raw = "raw"

    class PublicFormat:
        Raw = "raw"

    class NoEncryption:
        pass


class _FallbackEd25519PublicKey:
    def __init__(self, raw: bytes) -> None:
        if not isinstance(raw, bytes) or len(raw) != 32:
            raise ValueError("Ed25519 public key must be 32 bytes")
        self._raw = raw
        self._point = _decodepoint(raw)

    @classmethod
    def from_public_bytes(cls, data: bytes) -> "_FallbackEd25519PublicKey":
        return cls(data)

    def public_bytes(self, encoding: Any = None, format: Any = None) -> bytes:
        return self._raw

    def verify(self, signature: bytes, data: bytes) -> None:
        if not isinstance(signature, bytes) or len(signature) != 64:
            raise ValueError("Invalid signature length")
        r_bytes = signature[:32]
        s_int = int.from_bytes(signature[32:], "little")
        if s_int >= _L:
            raise ValueError("Signature scalar out of range")
        r_point = _decodepoint(r_bytes)
        k = int.from_bytes(hashlib.sha512(r_bytes + self._raw + data).digest(), "little") % _L
        lhs = _scalarmult(_B, s_int)
        rhs = _edwards_add(r_point, _scalarmult(self._point, k))
        if _encodepoint(lhs) != _encodepoint(rhs):
            raise ValueError("Signature verification failed")


class _FallbackEd25519PrivateKey:
    def __init__(self, seed: bytes) -> None:
        if not isinstance(seed, bytes) or len(seed) != 32:
            raise ValueError("Ed25519 private key must be 32 bytes")
        self._seed = seed
        h = hashlib.sha512(seed).digest()
        a = int.from_bytes(h[:32], "little")
        a &= (1 << 254) - 8
        a |= 1 << 254
        self._scalar = a
        self._prefix = h[32:]
        self._pub_bytes = _encodepoint(_scalarmult(_B, a))

    @classmethod
    def generate(cls) -> "_FallbackEd25519PrivateKey":
        return cls(secrets.token_bytes(32))

    @classmethod
    def from_private_bytes(cls, data: bytes) -> "_FallbackEd25519PrivateKey":
        return cls(data)

    def private_bytes(self, encoding: Any = None, format: Any = None, encryption_algorithm: Any = None) -> bytes:
        return self._seed

    def public_key(self) -> _FallbackEd25519PublicKey:
        return _FallbackEd25519PublicKey(self._pub_bytes)

    def sign(self, data: bytes) -> bytes:
        r = int.from_bytes(hashlib.sha512(self._prefix + data).digest(), "little") % _L
        r_bytes = _encodepoint(_scalarmult(_B, r))
        k = int.from_bytes(hashlib.sha512(r_bytes + self._pub_bytes + data).digest(), "little") % _L
        s = (r + k * self._scalar) % _L
        return r_bytes + s.to_bytes(32, "little")


def _crypto():
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey, Ed25519PublicKey,
        )
        from cryptography.hazmat.primitives import serialization
        return Ed25519PrivateKey, Ed25519PublicKey, serialization
    except ImportError:
        return _FallbackEd25519PrivateKey, _FallbackEd25519PublicKey, _FallbackSerialization


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(value: str) -> bytes:
    try:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except Exception as exc:
        raise IdentityError("invalid base64url key encoding") from exc


def public_key_fingerprint(public_key_bytes: bytes) -> str:
    """Return a stable SHA-256 fingerprint in lowercase hexadecimal."""
    if not isinstance(public_key_bytes, bytes) or len(public_key_bytes) != 32:
        raise IdentityError("Ed25519 public key must be exactly 32 bytes")
    return hashlib.sha256(public_key_bytes).hexdigest()


@dataclass(frozen=True, slots=True)
class Identity:
    """Public identity descriptor; contains no private key material."""
    id: str
    public_key: str
    algorithm: str = "Ed25519"
    fingerprint: str = ""

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise IdentityError("identity id is required")
        if self.algorithm != "Ed25519":
            raise IdentityError("only Ed25519 identities are supported")
        raw = _unb64(self.public_key)
        if len(raw) != 32:
            raise IdentityError("Ed25519 public key must be 32 bytes")
        expected = public_key_fingerprint(raw)
        if self.fingerprint and self.fingerprint != expected:
            raise IdentityError("public key fingerprint mismatch")
        object.__setattr__(self, "fingerprint", expected)

    @property
    def public_key_bytes(self) -> bytes:
        return _unb64(self.public_key)

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "public_key": self.public_key,
                "algorithm": self.algorithm, "fingerprint": self.fingerprint}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Identity":
        return cls(**value)


@dataclass(frozen=True, slots=True)
class KeyPair:
    identity: Identity
    private_key: str

    @property
    def private_key_bytes(self) -> bytes:
        return _unb64(self.private_key)

    def export_private_key(self) -> str:
        """Export private key as base64url raw bytes; protect this output."""
        return self.private_key


def generate_keypair(identity_id: str) -> KeyPair:
    if not identity_id or not identity_id.strip():
        raise IdentityError("identity id is required")
    Ed25519PrivateKey, _, serialization = _crypto()
    private = Ed25519PrivateKey.generate()
    private_bytes = private.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    identity = Identity(identity_id, _b64(public_bytes))
    return KeyPair(identity, _b64(private_bytes))


def identity_from_public_key(identity_id: str, public_key: bytes | str) -> Identity:
    if isinstance(public_key, str):
        raw = _unb64(public_key)
    else:
        raw = public_key
    return Identity(identity_id, _b64(raw))
