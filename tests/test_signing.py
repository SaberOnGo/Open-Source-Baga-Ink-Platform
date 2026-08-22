from __future__ import annotations

from datetime import datetime, timezone

import pytest

from baga_spec.canonical import canonical_sha256
from baga_spec.errors import SignatureError
from baga_spec.signing import build_files_manifest, verify_release_statement

PUBLISHER_ID = "pub1_fy3xxqegf6r7ns6e3x3nuxhcqvpcrrn3nue72jvfmzhf6c2kutmq"
APP_KEY_ID = "ed25519:ti6Gf6LzOv5i1daxZC4WIdVDMHhGsqV7iX5xCRm3Zwk"
APP_PUBLIC = "7UkoxijRwsbq6QM4kFmVYSlZJzpcY_k2NsFGFKyHN9E"

DELEGATION = {
    "type": "baga.app-key-delegation",
    "format": "0.1",
    "publisher_id": PUBLISHER_ID,
    "app_id": "com.example.reader",
    "delegation_sequence": 1,
    "key_id": APP_KEY_ID,
    "public_key": APP_PUBLIC,
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

SIGNATURES = {
    "type": "baga.signature-set",
    "format": "0.1",
    "signed_object": "signature/release-statement.json",
    "signed_object_sha256": "sha256:2cc388cf8b044ac663ba958430fcf5058998bf0fb73013bbd9f846244943cf8e",
    "signatures": [{
        "key_id": APP_KEY_ID,
        "algorithm": "ed25519",
        "signature": "gRMRfV0lBOeI9_7s2yFZtPywMNyv3jOJeoWrd_9NnvyJ6I_OGUKIMTf_YYk1P0E2_LnWgIBi3_q8iNd0aUbjAw",
    }],
}


def test_build_files_manifest_sorts_paths_and_hashes_bytes() -> None:
    manifest = build_files_manifest({"main.lua": b"print('hi')\n", "manifest.json": b"{}"})
    assert manifest["type"] == "baga.ikp-files"
    assert [item["path"] for item in manifest["files"]] == ["main.lua", "manifest.json"]
    assert manifest["files"][0]["length"] == len(b"print('hi')\n")
    assert manifest["files"][0]["sha256"].startswith("sha256:")


def test_release_statement_signature_is_accepted() -> None:
    verified = verify_release_statement(
        RELEASE,
        SIGNATURES,
        DELEGATION,
        at=datetime(2026, 8, 23, tzinfo=timezone.utc),
    )
    assert verified.app_id == "com.example.reader"
    assert verified.release_sequence == 1
    assert verified.statement_digest == canonical_sha256(RELEASE)


def test_release_statement_rejects_wrong_signature() -> None:
    invalid = {**SIGNATURES, "signatures": [{**SIGNATURES["signatures"][0], "signature": "A" * 86}]}
    with pytest.raises(SignatureError):
        verify_release_statement(
            RELEASE,
            invalid,
            DELEGATION,
            at=datetime(2026, 8, 23, tzinfo=timezone.utc),
        )


def test_release_statement_rejects_out_of_scope_channel() -> None:
    release = {**RELEASE, "channel": "beta"}
    signatures = {**SIGNATURES, "signed_object_sha256": canonical_sha256(release)}
    with pytest.raises(SignatureError, match="channel"):
        verify_release_statement(
            release,
            signatures,
            DELEGATION,
            at=datetime(2026, 8, 23, tzinfo=timezone.utc),
        )
