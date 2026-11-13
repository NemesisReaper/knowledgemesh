"""Unit tests for RFC 8785 JSON Canonicalization Scheme (JCS)."""

from __future__ import annotations

import unittest
from packages.okf.canonical_jcs import rfc8785_canonicalize


class TestRFC8785CanonicalJCS(unittest.TestCase):
    def test_key_sorting_utf16_code_units(self):
        """RFC 8785: Keys must be sorted by UTF-16 code units."""
        # Simple ascii
        data = {"b": 2, "a": 1, "c": 3}
        self.assertEqual(rfc8785_canonicalize(data), b'{"a":1,"b":2,"c":3}')

        # Unicode keys: BMP vs Supplementary characters
        # In UTF-16: \u00e9 (é, code unit 0x00E9) < \u03c0 (π, 0x03C0) < \uff41 (ａ, 0xFF41)
        data = {"\uff41": 1, "\u00e9": 2, "\u03c0": 3}
        self.assertEqual(rfc8785_canonicalize(data), b'{"\xc3\xa9":2,"\xcf\x80":3,"\xef\xbd\x81":1}')

    def test_number_formatting(self):
        """RFC 8785: Number formatting rules per ECMAScript specification."""
        # Integers
        self.assertEqual(rfc8785_canonicalize({"val": 0}), b'{"val":0}')
        self.assertEqual(rfc8785_canonicalize({"val": 42}), b'{"val":42}')
        self.assertEqual(rfc8785_canonicalize({"val": -100}), b'{"val":-100}')

        # Floats that are integer in value must format without decimal point
        self.assertEqual(rfc8785_canonicalize({"val": 1.0}), b'{"val":1}')
        self.assertEqual(rfc8785_canonicalize({"val": 1000.0}), b'{"val":1000}')

        # Negative zero must format as "0"
        self.assertEqual(rfc8785_canonicalize({"val": -0.0}), b'{"val":0}')

        # Standard decimal fractions
        self.assertEqual(rfc8785_canonicalize({"val": 3.14159}), b'{"val":3.14159}')

    def test_string_escaping(self):
        """RFC 8785: Only quotes, backslash, and 0x00-0x1F control characters are escaped."""
        # Forward slashes must NOT be escaped
        self.assertEqual(rfc8785_canonicalize({"url": "https://arxiv.org/abs/2401.18079"}),
                         b'{"url":"https://arxiv.org/abs/2401.18079"}')

        # Control characters
        data = {"text": "hello\nworld\t!\r\b\f"}
        self.assertEqual(rfc8785_canonicalize(data), b'{"text":"hello\\nworld\\t!\\r\\b\\f"}')

        # Quotes and backslashes
        data = {"msg": 'He said "Hello" and \\path'}
        self.assertEqual(rfc8785_canonicalize(data), b'{"msg":"He said \\"Hello\\" and \\\\path"}')

        # Unicode characters must remain literal UTF-8 bytes, not \\uXXXX escapes
        data = {"symbol": "€", "emoji": "🧠"}
        self.assertEqual(rfc8785_canonicalize(data), '{"emoji":"🧠","symbol":"€"}'.encode("utf-8"))

    def test_whitespace_elimination(self):
        """RFC 8785: No whitespace allowed outside strings."""
        data = {
            "arr": [1, 2, 3],
            "nested": {"x": True, "y": None, "z": False}
        }
        expected = b'{"arr":[1,2,3],"nested":{"x":true,"y":null,"z":false}}'
        self.assertEqual(rfc8785_canonicalize(data), expected)

    def test_deterministic_identical_bytes(self):
        """Different dictionary insertion orders produce the exact same byte string."""
        d1 = {"z": 100, "a": {"k2": "v2", "k1": "v1"}, "m": [3, 2, 1]}
        d2 = {"a": {"k1": "v1", "k2": "v2"}, "m": [3, 2, 1], "z": 100}
        self.assertEqual(rfc8785_canonicalize(d1), rfc8785_canonicalize(d2))


if __name__ == "__main__":
    unittest.main()

