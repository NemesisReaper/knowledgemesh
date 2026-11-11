from __future__ import annotations
from uuid import uuid4
import re

_ID_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")

def new_id(prefix: str | None=None) -> str:
    """Create a UUID4 identifier, optionally namespaced with a validated prefix."""
    value=str(uuid4())
    if prefix is None: return value
    validate_id(prefix)
    return f"{prefix}:{value}"

def validate_id(value: str) -> str:
    if not isinstance(value,str) or not _ID_RE.fullmatch(value):
        raise ValueError("ID must be 1-128 characters: letters, digits, '.', '_', ':', '-'")
    return value
