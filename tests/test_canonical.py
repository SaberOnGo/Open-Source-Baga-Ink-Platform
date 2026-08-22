from __future__ import annotations

from pathlib import Path

from baga_spec.canonical import canonical_sha256, canonicalize
from baga_spec.strict_json import loads_strict

ROOT = Path(__file__).resolve().parents[1]
VECTOR_ROOT = ROOT / "spec" / "vectors" / "canonical-json"


def test_canonicalizes_object_keys_in_rfc8785_order() -> None:
    assert canonicalize({"b": 1, "a": 2}) == b'{"a":2,"b":1}'


def test_canonicalizes_unicode_without_ascii_escaping() -> None:
    assert canonicalize({"text": "雪"}) == '{"text":"雪"}'.encode("utf-8")


def test_canonical_sha256_is_prefixed_lowercase_hex() -> None:
    assert canonical_sha256({"b": 1, "a": 2}) == (
        "sha256:d3626ac30a87e6f7a6428233b3c68299976865fa5508e4267c5415c76af7a772"
    )


def test_checked_in_canonical_vectors() -> None:
    vector_dirs = sorted(path for path in VECTOR_ROOT.iterdir() if path.is_dir())
    assert vector_dirs, "canonical vector corpus must not be empty"
    for vector_dir in vector_dirs:
        value = loads_strict((vector_dir / "input.json").read_bytes())
        expected_bytes = bytes.fromhex((vector_dir / "canonical.hex").read_text().strip())
        expected_hash = (vector_dir / "sha256.txt").read_text().strip()
        assert canonicalize(value) == expected_bytes, vector_dir.name
        assert canonical_sha256(value) == expected_hash, vector_dir.name
