from __future__ import annotations

import json
import warnings
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from baga_spec.canonical import canonical_sha256, canonicalize
from baga_spec.crypto import (
    b64u_encode,
    ed25519_key_id,
    ed25519_public_key_from_seed,
    sha256_digest,
    sign_ed25519,
)
from baga_spec.errors import IKPError
from baga_spec.identity import publisher_id
from baga_spec.ikp import verify_ikp
from baga_spec.signing import build_files_manifest

ROOT_SEED = bytes.fromhex("01" * 32)
RECOVERY_SEED = bytes.fromhex("02" * 32)
APP_SEED = bytes.fromhex("03" * 32)


def _json_bytes(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _key(seed: bytes) -> tuple[str, str]:
    public = ed25519_public_key_from_seed(seed)
    return ed25519_key_id(public), b64u_encode(public)


def _signature_set(path: str, statement: dict, seed: bytes, key_id: str) -> dict:
    return {
        "type": "baga.signature-set",
        "format": "0.1",
        "signed_object": path,
        "signed_object_sha256": canonical_sha256(statement),
        "signatures": [{
            "key_id": key_id,
            "algorithm": "ed25519",
            "signature": b64u_encode(sign_ed25519(seed, canonicalize(statement))),
        }],
    }


def build_signed_ikp(path: Path, *, tamper_payload: bool = False, release_version: str = "1.0.0", add_native: bool = False) -> None:
    root_key_id, root_public = _key(ROOT_SEED)
    recovery_key_id, recovery_public = _key(RECOVERY_SEED)
    app_key_id, app_public = _key(APP_SEED)

    genesis = {
        "type": "baga.publisher-genesis",
        "format": "0.1",
        "display_name": "Example Studio",
        "root_threshold": 1,
        "root_keys": [{"key_id": root_key_id, "algorithm": "ed25519", "public_key": root_public}],
        "recovery_threshold": 1,
        "recovery_keys": [{"key_id": recovery_key_id, "algorithm": "ed25519", "public_key": recovery_public}],
        "created_at": "2026-08-22T00:00:00Z",
    }
    pub_id = publisher_id(genesis)
    ownership = {
        "type": "baga.app-ownership",
        "format": "0.1",
        "publisher_id": pub_id,
        "app_id": "com.example.reader",
        "ownership_sequence": 1,
        "status": "active",
        "created_at": "2026-08-22T00:00:00Z",
    }
    delegation = {
        "type": "baga.app-key-delegation",
        "format": "0.1",
        "publisher_id": pub_id,
        "app_id": "com.example.reader",
        "delegation_sequence": 1,
        "key_id": app_key_id,
        "public_key": app_public,
        "signature_threshold": 1,
        "allowed_channels": ["stable"],
        "min_release_sequence": 1,
        "max_release_sequence": 100,
        "valid_from": "2026-08-22T00:00:00Z",
        "valid_until": "2027-08-22T00:00:00Z",
        "status": "active",
    }
    manifest = {
        "ikp_format": "0.4",
        "id": "com.example.reader",
        "name": "Example Reader",
        "version_name": "1.0.0",
        "release_sequence": 1,
        "channel": "stable",
        "entry": "main.lua",
        "baga_api": {"min": "0.2", "max_exclusive": "1.0"},
        "permissions": [],
        "capabilities": {"required": ["display.basic"], "optional": []},
        "data_schema_version": 1,
        "rollback": {"mode": "safe", "minimum_compatible_schema": 1},
    }
    payload = {
        "manifest.json": _json_bytes(manifest),
        "main.lua": b"print('hello baga ink')\n",
    }
    if add_native:
        payload["native/module.so"] = b"\x7fELF" + b"x" * 16
    files_manifest = build_files_manifest(payload)
    files_bytes = _json_bytes(files_manifest)
    manifest_bytes = payload["manifest.json"]

    release = {
        "type": "baga.ikp-release",
        "format": "0.1",
        "app_id": manifest["id"],
        "publisher_id": pub_id,
        "version_name": release_version,
        "release_sequence": manifest["release_sequence"],
        "channel": manifest["channel"],
        "ikp_format": manifest["ikp_format"],
        "baga_api": manifest["baga_api"],
        "manifest": {"path": "manifest.json", "length": len(manifest_bytes), "sha256": sha256_digest(manifest_bytes)},
        "files_manifest": {"path": "signature/files.json", "length": len(files_bytes), "sha256": sha256_digest(files_bytes)},
        "publisher_identity_digest": canonical_sha256(genesis),
        "app_ownership_digest": canonical_sha256(ownership),
        "app_key_delegation_digest": canonical_sha256(delegation),
        "app_signing_key_id": app_key_id,
        "created_at": "2026-08-22T00:00:00Z",
    }

    entries = {
        **payload,
        "signature/files.json": files_bytes,
        "signature/publisher-genesis.json": _json_bytes(genesis),
        "signature/app-ownership.json": _json_bytes(ownership),
        "signature/app-ownership.signatures.json": _json_bytes(_signature_set("signature/app-ownership.json", ownership, ROOT_SEED, root_key_id)),
        "signature/app-key-delegation.json": _json_bytes(delegation),
        "signature/app-key-delegation.signatures.json": _json_bytes(_signature_set("signature/app-key-delegation.json", delegation, ROOT_SEED, root_key_id)),
        "signature/release-statement.json": _json_bytes(release),
        "signature/release.signatures.json": _json_bytes(_signature_set("signature/release-statement.json", release, APP_SEED, app_key_id)),
    }
    if tamper_payload:
        entries["main.lua"] = b"print('tampered')\n"

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(entries):
            archive.writestr(name, entries[name])


def test_valid_signed_ikp_is_accepted(tmp_path: Path) -> None:
    ikp = tmp_path / "reader.ikp"
    build_signed_ikp(ikp)
    result = verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))
    assert result.app_id == "com.example.reader"
    assert result.release_sequence == 1
    assert result.publisher_id.startswith("pub1_")


def test_tampered_payload_is_rejected(tmp_path: Path) -> None:
    ikp = tmp_path / "tampered.ikp"
    build_signed_ikp(ikp, tamper_payload=True)
    with pytest.raises(IKPError, match="payload"):
        verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))


def test_release_manifest_version_mismatch_is_rejected(tmp_path: Path) -> None:
    ikp = tmp_path / "mismatch.ikp"
    build_signed_ikp(ikp, release_version="2.0.0")
    with pytest.raises(IKPError, match="version_name"):
        verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))


def test_native_executable_dependency_is_rejected(tmp_path: Path) -> None:
    ikp = tmp_path / "native.ikp"
    build_signed_ikp(ikp, add_native=True)
    with pytest.raises(IKPError, match="native executable"):
        verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))


def test_duplicate_zip_entry_is_rejected(tmp_path: Path) -> None:
    ikp = tmp_path / "duplicate.ikp"
    build_signed_ikp(ikp)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(ikp, "a") as archive:
            archive.writestr("main.lua", b"duplicate")
    with pytest.raises(IKPError, match="duplicate ZIP entry"):
        verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))


def test_path_traversal_entry_is_rejected(tmp_path: Path) -> None:
    ikp = tmp_path / "traversal.ikp"
    build_signed_ikp(ikp)
    with zipfile.ZipFile(ikp, "a") as archive:
        archive.writestr("../escape", b"bad")
    with pytest.raises(IKPError, match="unsafe ZIP path"):
        verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))
