from __future__ import annotations

import copy

import pytest

from baga_spec.errors import SchemaValidationError
from baga_spec.schemas import validate_schema

GENESIS = {
    "type": "baga.publisher-genesis",
    "format": "0.1",
    "display_name": "Example Studio",
    "root_threshold": 1,
    "root_keys": [
        {
            "key_id": "ed25519:" + "11" * 32,
            "algorithm": "ed25519",
            "public_key": "A" * 43,
        }
    ],
    "recovery_threshold": 1,
    "recovery_keys": [
        {
            "key_id": "ed25519:" + "22" * 32,
            "algorithm": "ed25519",
            "public_key": "B" * 43,
        }
    ],
    "created_at": "2026-08-22T00:00:00Z",
}

OWNERSHIP = {
    "type": "baga.app-ownership",
    "format": "0.1",
    "publisher_id": "pub1_" + "a" * 52,
    "app_id": "com.example.reader",
    "ownership_sequence": 1,
    "created_at": "2026-08-22T00:00:00Z",
}

DELEGATION = {
    "type": "baga.app-key-delegation",
    "format": "0.1",
    "publisher_id": "pub1_" + "a" * 52,
    "app_id": "com.example.reader",
    "delegation_sequence": 1,
    "key_id": "ed25519:" + "33" * 32,
    "public_key": "C" * 43,
    "channels": ["stable"],
    "release_sequence_min": 1,
    "release_sequence_max": 100,
    "valid_from": "2026-08-22T00:00:00Z",
    "expires": "2027-08-22T00:00:00Z",
}

RELEASE = {
    "type": "baga.release-statement",
    "format": "0.1",
    "publisher_id": "pub1_" + "a" * 52,
    "app_id": "com.example.reader",
    "release_sequence": 1,
    "version_name": "1.0.0",
    "channel": "stable",
    "package_sha256": "sha256:" + "44" * 32,
    "package_length": 1024,
    "manifest_sha256": "sha256:" + "55" * 32,
    "permissions": ["network"],
    "capabilities": {"required": ["display.basic"], "optional": []},
    "data_schema_version": 1,
    "created_at": "2026-08-22T00:00:00Z",
}

TRANSFER = {
    "type": "baga.transfer-session",
    "format": "0.1",
    "session_id": "session-123",
    "repository_id": "repo1_" + "b" * 52,
    "created_at": "2026-08-22T00:00:00Z",
    "items": [
        {
            "kind": "ikp",
            "path": "packages/sha256/aa/app.ikp",
            "length": 1024,
            "sha256": "sha256:" + "66" * 32,
            "app_id": "com.example.reader",
            "release_sequence": 1,
        }
    ],
}


@pytest.mark.parametrize(
    ("schema_name", "instance"),
    [
        ("publisher-genesis", GENESIS),
        ("app-ownership", OWNERSHIP),
        ("app-key-delegation", DELEGATION),
        ("release-statement", RELEASE),
        ("transfer-session", TRANSFER),
    ],
)
def test_accepts_valid_security_objects(schema_name: str, instance: dict) -> None:
    validate_schema(schema_name, instance)


def test_rejects_unknown_security_critical_field() -> None:
    invalid = copy.deepcopy(OWNERSHIP)
    invalid["unexpected"] = True
    with pytest.raises(SchemaValidationError, match="unexpected"):
        validate_schema("app-ownership", invalid)


def test_rejects_non_utc_timestamp() -> None:
    invalid = copy.deepcopy(GENESIS)
    invalid["created_at"] = "2026-08-22T08:00:00+08:00"
    with pytest.raises(SchemaValidationError):
        validate_schema("publisher-genesis", invalid)


def test_rejects_malformed_digest() -> None:
    invalid = copy.deepcopy(RELEASE)
    invalid["package_sha256"] = "sha256:ABC"
    with pytest.raises(SchemaValidationError):
        validate_schema("release-statement", invalid)
