from __future__ import annotations
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timezone
from enum import Enum
from uuid import UUID
from typing import Any, Mapping
import hashlib, json

def to_primitive(value: Any) -> Any:
    """Convert supported Python values into deterministic JSON-compatible values."""
    if is_dataclass(value): return to_primitive(asdict(value))
    if isinstance(value,Enum): return to_primitive(value.value)
    if isinstance(value,datetime):
        if value.tzinfo is None: raise ValueError("naive datetimes are not serializable")
        return value.astimezone(timezone.utc).isoformat().replace("+00:00","Z")
    if isinstance(value,date): return value.isoformat()
    if isinstance(value,UUID): return str(value)
    if isinstance(value,Mapping):
        if not all(isinstance(k,str) for k in value): raise TypeError("JSON object keys must be strings")
        return {k:to_primitive(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [to_primitive(v) for v in value]
    if isinstance(value,(str,int,float,bool)) or value is None:
        if isinstance(value,float):
            import math
            if not math.isfinite(value): raise ValueError("non-finite floats are not supported")
        return value
    raise TypeError(f"unsupported serialization type: {type(value).__name__}")

def canonical_json(value: Any) -> str:
    return json.dumps(to_primitive(value),sort_keys=True,separators=(",",":"),
                      ensure_ascii=False,allow_nan=False)

def stable_hash(value: Any, algorithm: str="sha256") -> str:
    if algorithm not in {"sha256","sha512"}: raise ValueError("algorithm must be sha256 or sha512")
    digest=hashlib.new(algorithm,canonical_json(value).encode("utf-8")).hexdigest()
    return f"{algorithm}:{digest}"
