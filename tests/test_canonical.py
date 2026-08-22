from __future__ import annotations

from baga_spec.canonical import canonical_sha256, canonicalize


def test_canonicalizes_object_keys_in_rfc8785_order() -> None:
    assert canonicalize({"b": 1, "a": 2}) == b'{"a":2,"b":1}'


def test_canonicalizes_unicode_without_ascii_escaping() -> None:
    assert canonicalize({"text": "雪"}) == '{"text":"雪"}'.encode("utf-8")


def test_canonical_sha256_is_prefixed_lowercase_hex() -> None:
    assert canonical_sha256({"b": 1, "a": 2}) == (
        "sha256:d3626ac30a87e6f7a6428233b3c68299976865fa5508e4267c5415c76af7a772"
    )
