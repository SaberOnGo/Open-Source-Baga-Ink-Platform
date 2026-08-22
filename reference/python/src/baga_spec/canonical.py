from __future__ import annotations

import hashlib
from typing import Any

import rfc8785

from .errors import BagaSpecError


class CanonicalizationError(BagaSpecError):
    code = "canonicalization_error"


def canonicalize(value: Any) -> bytes:
    try:
        encoded = rfc8785.dumps(value)
    except Exception as exc:  # rfc8785 exposes implementation-specific error subclasses
        raise CanonicalizationError(str(exc)) from exc
    if not isinstance(encoded, bytes):
        encoded = bytes(encoded)
    return encoded


def canonical_sha256(value: Any) -> str:
    digest = hashlib.sha256(canonicalize(value)).hexdigest()
    return f"sha256:{digest}"
