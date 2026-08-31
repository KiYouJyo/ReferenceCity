from __future__ import annotations

import hashlib

import rfc8785


def canonical_bytes(value: object) -> bytes:
    """Serialize JSON-compatible data using RFC 8785 JSON Canonicalization Scheme."""
    return rfc8785.dumps(value)


def canonical_sha256(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()
