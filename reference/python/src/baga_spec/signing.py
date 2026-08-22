from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Mapping

from .canonical import canonical_sha256, canonicalize
from .crypto import b64u_decode, ed25519_key_id, sha256_digest, verify_ed25519
from .errors import SignatureError
from .schemas import validate_schema


@dataclass(frozen=True)
class VerifiedRelease:
    app_id: str
    publisher_id: str
    release_sequence: int
    channel: str
    signing_key_id: str
    statement_digest: str


def _safe_payload_path(path: str) -> bool:
    candidate = PurePosixPath(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts and not path.startswith("signature/")


def build_files_manifest(entries: Mapping[str, bytes]) -> dict:
    if not entries:
        raise SignatureError("IKP payload file set cannot be empty")
    files: list[dict] = []
    for path in sorted(entries, key=lambda value: value.encode("utf-8")):
        data = entries[path]
        if not _safe_payload_path(path):
            raise SignatureError(f"unsafe payload path: {path}")
        if not isinstance(data, bytes):
            raise SignatureError(f"payload value for {path} must be bytes")
        files.append({"path": path, "length": len(data), "sha256": sha256_digest(data)})
    result = {
        "type": "baga.ikp-files",
        "format": "0.1",
        "hash_algorithm": "sha256",
        "files": files,
    }
    validate_schema("files-manifest", result)
    return result


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise SignatureError(f"invalid UTC timestamp: {value}") from exc
    return parsed.replace(tzinfo=timezone.utc)


def verify_release_statement(
    release: dict,
    signature_set: dict,
    delegation: dict,
    *,
    at: datetime,
) -> VerifiedRelease:
    validate_schema("ikp-release", release)
    validate_schema("signature-set", signature_set)
    validate_schema("app-key-delegation", delegation)

    if release["publisher_id"] != delegation["publisher_id"]:
        raise SignatureError("release publisher_id does not match delegation")
    if release["app_id"] != delegation["app_id"]:
        raise SignatureError("release app_id does not match delegation")
    if release["app_signing_key_id"] != delegation["key_id"]:
        raise SignatureError("release signing key does not match delegation")
    if delegation["status"] != "active":
        raise SignatureError("app signing delegation is not active")
    if release["channel"] not in delegation["allowed_channels"]:
        raise SignatureError("release channel is outside delegation scope")
    if not delegation["min_release_sequence"] <= release["release_sequence"] <= delegation["max_release_sequence"]:
        raise SignatureError("release sequence is outside delegation scope")

    if at.tzinfo is None:
        raise SignatureError("verification time must be timezone-aware")
    check_time = at.astimezone(timezone.utc)
    if check_time < _parse_utc(delegation["valid_from"]):
        raise SignatureError("delegation is not yet valid")
    if check_time >= _parse_utc(delegation["valid_until"]):
        raise SignatureError("delegation expired")

    public_key = b64u_decode(delegation["public_key"])
    if ed25519_key_id(public_key) != delegation["key_id"]:
        raise SignatureError("delegated key_id does not match public key")

    statement_digest = canonical_sha256(release)
    if signature_set["signed_object_sha256"] != statement_digest:
        raise SignatureError("signature set object digest mismatch")

    message = canonicalize(release)
    valid_key_ids: set[str] = set()
    for item in signature_set["signatures"]:
        if item["key_id"] != delegation["key_id"] or item["key_id"] in valid_key_ids:
            continue
        try:
            verify_ed25519(public_key, message, b64u_decode(item["signature"]))
        except SignatureError:
            continue
        valid_key_ids.add(item["key_id"])

    threshold = delegation["signature_threshold"]
    if threshold != 1:
        raise SignatureError("v0.1 executable profile supports one delegated release key per delegation")
    if len(valid_key_ids) < threshold:
        raise SignatureError("release signature threshold not met")

    return VerifiedRelease(
        app_id=release["app_id"],
        publisher_id=release["publisher_id"],
        release_sequence=release["release_sequence"],
        channel=release["channel"],
        signing_key_id=delegation["key_id"],
        statement_digest=statement_digest,
    )
