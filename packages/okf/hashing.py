"""Deterministic cryptographic hashing and canonicalization for the Open Knowledge Format (OKF)."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from .canonical_jcs import rfc8785_canonicalize


def _json_default(obj: Any) -> Any:
    """JSON serializer for types not serializable by default json code."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "value"):  # Enum support
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable to canonical JSON")


def canonicalize_json(data: dict[str, Any] | BaseModel) -> bytes:
    """Produce deterministic UTF-8 encoded canonical JSON strictly conforming to RFC 8785 JCS.

    Keys are recursively sorted by UTF-16 code units and whitespace is eliminated.
    """
    return rfc8785_canonicalize(data)


def hash_bytes(data: bytes, algorithm: str = "sha256") -> str:
    """Compute cryptographic hash of raw bytes.

    Returns hash string with algorithm prefix, e.g. 'sha256:<hex>'.
    """
    hasher = hashlib.new(algorithm)
    hasher.update(data)
    return f"{algorithm}:{hasher.hexdigest()}"


def hash_file(file_path: Path | str, algorithm: str = "sha256", chunk_size: int = 65536) -> str:
    """Compute cryptographic hash of a file on disk."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found for hashing: {file_path}")

    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return f"{algorithm}:{hasher.hexdigest()}"


def calculate_canonical_hash(data: dict[str, Any] | BaseModel, algorithm: str = "sha256") -> str:
    """Compute deterministic content hash of structured data or Pydantic model."""
    canonical_bytes = canonicalize_json(data)
    return hash_bytes(canonical_bytes, algorithm=algorithm)


def verify_hash(data: dict[str, Any] | BaseModel | bytes, expected_hash: str) -> bool:
    """Verify that data matches the expected content hash (e.g. 'sha256:<hex>')."""
    if ":" in expected_hash:
        algorithm, _ = expected_hash.split(":", 1)
    else:
        algorithm = "sha256"
        expected_hash = f"sha256:{expected_hash}"

    if isinstance(data, bytes):
        computed = hash_bytes(data, algorithm=algorithm)
    else:
        computed = calculate_canonical_hash(data, algorithm=algorithm)

    return computed.lower() == expected_hash.lower()


def compute_merkle_root(hashes: list[str], algorithm: str = "sha256") -> str:
    """Compute the Merkle root hash from an ordered list of leaf hashes."""
    if not hashes:
        return hash_bytes(b"", algorithm=algorithm)

    current_level = [
        bytes.fromhex(h.split(":")[-1]) for h in sorted(hashes)
    ]

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            hasher = hashlib.new(algorithm)
            hasher.update(left + right)
            next_level.append(hasher.digest())
        current_level = next_level

    return f"{algorithm}:{current_level[0].hex()}"

