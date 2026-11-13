"""RFC 8785 JSON Canonicalization Scheme (JCS) implementation.

Strict implementation of RFC 8785 (https://tools.ietf.org/html/rfc8785):
- UTF-8 output encoding
- Whitespace elimination
- Strict UTF-16 code unit object key sorting
- IEEE 754 floating point and integer canonical representation (ECMAScript compatible)
- Minimal RFC 8785 string escaping (quotation mark, reverse solidus, control characters)
"""

from __future__ import annotations

from datetime import datetime, date
import math
from pathlib import Path
from typing import Any
from pydantic import BaseModel


def _format_jcs_number(val: int | float) -> str:
    """Format integer or float per RFC 8785 Section 3.2.2.3 and ECMAScript Number::toString(10)."""
    if isinstance(val, bool):
        return "true" if val else "false"

    if isinstance(val, int):
        return str(val)

    # Float handling
    if math.isnan(val) or math.isinf(val):
        raise ValueError("NaN and Infinity are not valid JSON numbers per RFC 8785")

    # In RFC 8785, negative zero must serialize as "0"
    if val == 0.0:
        return "0"

    # If it is an integer in value (e.g. 1.0 or 42.0), format without decimal point
    if val.is_integer() and abs(val) < 1e21:
        return str(int(val))

    # General float formatting adhering to ECMAScript Number::toString(10)
    # Using Python float repr which uses the David Gay dtoa / Ryu algorithm for shortest round-trip
    s = repr(val)
    
    # Handle exponent notation differences between Python and JS
    if "e" in s or "E" in s:
        mantissa, exp_str = s.lower().split("e")
        exp_val = int(exp_str)
        # JavaScript adds '+' for positive exponents
        sign_str = "+" if exp_val >= 0 else "-"
        return f"{mantissa}e{sign_str}{abs(exp_val)}"

    # If the float representation ends in .0, strip it
    if s.endswith(".0"):
        return s[:-2]

    return s


def _escape_jcs_string(s: str) -> str:
    """Escape string according to RFC 8785 Section 3.2.2.2.
    
    Only quote, backslash, and control characters 0x00-0x1F are escaped.
    All other characters (including forward slash and multi-byte UTF-8) are unescaped.
    """
    out = ['"']
    for char in s:
        code = ord(char)
        if char == '"':
            out.append(r'\"')
        elif char == '\\':
            out.append(r'\\')
        elif char == '\b':
            out.append(r'\b')
        elif char == '\f':
            out.append(r'\f')
        elif char == '\n':
            out.append(r'\n')
        elif char == '\r':
            out.append(r'\r')
        elif char == '\t':
            out.append(r'\t')
        elif code < 0x20:
            out.append(f"\\u{code:04x}")
        else:
            out.append(char)
    out.append('"')
    return "".join(out)


def _serialize_jcs_value(val: Any) -> str:
    """Recursively serialize a Python object to an RFC 8785 canonical JSON string."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return _format_jcs_number(val)
    if isinstance(val, str):
        return _escape_jcs_string(val)
    if isinstance(val, (datetime, date)):
        return _escape_jcs_string(val.isoformat())
    if isinstance(val, Path):
        return _escape_jcs_string(str(val))
    if hasattr(val, "value") and not isinstance(val, type):  # Enum support
        return _serialize_jcs_value(val.value)
    if isinstance(val, BaseModel):
        return _serialize_jcs_value(val.model_dump(mode="json"))
    if isinstance(val, (list, tuple)):
        items = [_serialize_jcs_value(item) for item in val]
        return "[" + ",".join(items) + "]"
    if isinstance(val, dict):
        # RFC 8785 Section 3.2.3: Sort object keys by UTF-16 code units
        # Sorting by key.encode('utf-16-be') yields exact UTF-16 code unit ordering
        sorted_keys = sorted(val.keys(), key=lambda k: str(k).encode("utf-16-be"))
        entries = []
        for k in sorted_keys:
            key_str = _escape_jcs_string(str(k))
            val_str = _serialize_jcs_value(val[k])
            entries.append(f"{key_str}:{val_str}")
        return "{" + ",".join(entries) + "}"

    raise TypeError(f"Type {type(val)} is not serializable to RFC 8785 canonical JSON")


def rfc8785_canonicalize(data: Any) -> bytes:
    """Produce deterministic UTF-8 encoded canonical JSON strictly conforming to RFC 8785 JCS.
    
    Args:
        data: Arbitrary JSON-serializable Python data structure, dict, or Pydantic model.
        
    Returns:
        Canonical UTF-8 encoded bytes.
    """
    canonical_str = _serialize_jcs_value(data)
    return canonical_str.encode("utf-8")

