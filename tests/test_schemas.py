from __future__ import annotations

import copy

import pytest

from baga_spec.errors import SchemaValidationError
from baga_spec.schemas import schema_path, validate_schema

EXPECTED_SCHEMAS = [
    "publisher-genesis",
    "publisher-identity",
    "app-ownership",
    "app-key-delegation",
    "app-transfer",
    "files-manifest",
    "ikp-release",
    "signature-set",
    "release-record",
    "baga-target-custom",
    "review-attestation",
    "revocation-statement",
    "update-journal",
    "transfer-session",
    "offline-snapshot-manifest",
    "transparency-event",
    "transparency-checkpoint",
    "catalog-root",
    "catalog-app-record",
    "catalog-diff",
]

PUBLISHER_ID = "pub1_fy3xxqegf6r7ns6e3x3nuxhcqvpcrrn3nue72jvfmzhf6c2kutmq"
ROOT_KEY_ID = "ed25519:NHUPmL1Z_PyUbaRaqr6TO-FUpLUJThxKv0KGZQXzyX4"
RECOVERY_KEY_ID = "ed25519:ajgD1fBZkCocba-8m6RykhL3yqwIY0zDrnaydSnwOCc"
APP_KEY_ID = "ed25519:ti6Gf6LzOv5i1daxZC4WIdVDMHhGsqV7iX5xCRm3Zwk"

GENESIS = {
    "type": "baga.publisher-genesis",
    "format": "0.1",
    "display_name": "Example Studio",
    "root_threshold": 1,
    "root_keys": [{"key_id": ROOT_KEY_ID, "algorithm": "ed25519", "public_key": "iojj3XQJ8ZX9UtstPLpdcspnCb8dlBIb83SIAbQPb1w"}],
    "recovery_threshold": 1,
    "recovery_keys": [{"key_id": RECOVERY_KEY_ID, "algorithm": "ed25519", "public_key": "gTl3Dqh9F19Wo1Rmw0x-zMuNipG07jeiXfYPW4_Js5Q"}],
    "created_at": "2026-08-22T00:00:00Z",
}

OWNERSHIP = {
    "type": "baga.app-ownership",
    "format": "0.1",
    "publisher_id": PUBLISHER_ID,
    "app_id": "com.example.reader",
    "ownership_sequence": 1,
    "status": "active",
    "created_at": "2026-08-22T00:00:00Z",
}

DELEGATION = {
    "type": "baga.app-key-delegation",
    "format": "0.1",
    "publisher_id": PUBLISHER_ID,
    "app_id": "com.example.reader",
    "delegation_sequence": 1,
    "key_id": APP_KEY_ID,
    "public_key": "7UkoxijRwsbq6QM4kFmVYSlZJzpcY_k2NsFGFKyHN9E",
    "signature_threshold": 1,
    "allowed_channels": ["stable"],
    "min_release_sequence": 1,
    "max_release_sequence": 100,
    "valid_from": "2026-08-22T00:00:00Z",
    "valid_until": "2027-08-22T00:00:00Z",
    "status": "active",
}

RELEASE = {
    "type": "baga.ikp-release",
    "format": "0.1",
    "app_id": "com.example.reader",
    "publisher_id": PUBLISHER_ID,
    "version_name": "1.0.0",
    "release_sequence": 1,
    "channel": "stable",
    "ikp_format": "0.4",
    "baga_api": {"min": "0.2", "max_exclusive": "1.0"},
    "manifest": {"path": "manifest.json", "length": 200, "sha256": "sha256:" + "11" * 32},
    "files_manifest": {"path": "signature/files.json", "length": 300, "sha256": "sha256:" + "22" * 32},
    "publisher_identity_digest": "sha256:" + "33" * 32,
    "app_ownership_digest": "sha256:" + "44" * 32,
    "app_key_delegation_digest": "sha256:" + "55" * 32,
    "app_signing_key_id": APP_KEY_ID,
    "created_at": "2026-08-22T00:00:00Z",
}

TRANSFER = {
    "type": "baga.transfer-session",
    "format": "0.1",
    "session_id": "session-123",
    "repository_id": "repo1_" + "b" * 52,
    "created_at": "2026-08-22T00:00:00Z",
    "items": [{"kind": "ikp", "path": "packages/sha256/aa/app.ikp", "length": 1024, "sha256": "sha256:" + "66" * 32, "app_id": "com.example.reader", "release_sequence": 1}],
}


def test_all_executable_spec_schemas_are_registered() -> None:
    for name in EXPECTED_SCHEMAS:
        assert schema_path(name).is_file(), name


@pytest.mark.parametrize(
    ("schema_name", "instance"),
    [
        ("publisher-genesis", GENESIS),
        ("app-ownership", OWNERSHIP),
        ("app-key-delegation", DELEGATION),
        ("ikp-release", RELEASE),
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
    invalid["manifest"]["sha256"] = "sha256:ABC"
    with pytest.raises(SchemaValidationError):
        validate_schema("ikp-release", invalid)
