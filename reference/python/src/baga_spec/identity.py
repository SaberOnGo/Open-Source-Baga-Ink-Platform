from __future__ import annotations

import base64
import hashlib
from datetime import datetime, timezone
from typing import Any

from .canonical import canonicalize
from .crypto import b64u_decode, ed25519_key_id, verify_ed25519
from .errors import IdentityError, SignatureError
from .schemas import validate_schema


def _b32lower(data: bytes) -> str:
    return base64.b32encode(data).rstrip(b"=").decode("ascii").lower()


def publisher_id(genesis: dict[str, Any]) -> str:
    validate_schema("publisher-genesis", genesis)
    digest = hashlib.sha256(canonicalize(genesis)).digest()
    return "pub1_" + _b32lower(digest)


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise IdentityError(f"invalid UTC timestamp: {value}") from exc
    return parsed.replace(tzinfo=timezone.utc)


def _root_keys(genesis: dict[str, Any]) -> tuple[dict[str, bytes], int]:
    keys: dict[str, bytes] = {}
    for item in genesis["root_keys"]:
        public = b64u_decode(item["public_key"])
        actual = ed25519_key_id(public)
        if actual != item["key_id"]:
            raise IdentityError("root key_id does not match public key")
        keys[item["key_id"]] = public
    threshold = genesis["root_threshold"]
    if threshold > len(keys):
        raise IdentityError("root threshold exceeds available root keys")
    return keys, threshold


def _verify_root_threshold(
    genesis: dict[str, Any],
    statement: dict[str, Any],
    envelope: dict[str, Any],
) -> None:
    validate_schema("publisher-genesis", genesis)
    validate_schema("signature-envelope", envelope)
    signed_type = statement.get("type")
    if envelope["signed_type"] != signed_type:
        raise IdentityError("signature envelope signed_type mismatch")

    keys, threshold = _root_keys(genesis)
    message = canonicalize(statement)
    accepted: set[str] = set()
    for signature_item in envelope["signatures"]:
        key_id = signature_item["key_id"]
        if key_id in accepted or key_id not in keys:
            continue
        try:
            verify_ed25519(
                keys[key_id],
                message,
                b64u_decode(signature_item["signature"]),
            )
        except SignatureError:
            continue
        accepted.add(key_id)

    if len(accepted) < threshold:
        raise IdentityError(
            f"root signature threshold not met: {len(accepted)}/{threshold}"
        )


def verify_app_ownership(
    genesis: dict[str, Any],
    ownership: dict[str, Any],
    envelope: dict[str, Any],
) -> None:
    validate_schema("publisher-genesis", genesis)
    validate_schema("app-ownership", ownership)
    expected_publisher = publisher_id(genesis)
    if ownership["publisher_id"] != expected_publisher:
        raise IdentityError("app ownership publisher_id mismatch")
    _verify_root_threshold(genesis, ownership, envelope)


def verify_app_key_delegation(
    genesis: dict[str, Any],
    delegation: dict[str, Any],
    envelope: dict[str, Any],
    *,
    app_id: str,
    channel: str,
    release_sequence: int,
    at: datetime,
) -> None:
    validate_schema("publisher-genesis", genesis)
    validate_schema("app-key-delegation", delegation)
    expected_publisher = publisher_id(genesis)
    if delegation["publisher_id"] != expected_publisher:
        raise IdentityError("app key delegation publisher_id mismatch")
    if delegation["app_id"] != app_id:
        raise IdentityError("app key delegation app_id mismatch")

    public_key = b64u_decode(delegation["public_key"])
    if ed25519_key_id(public_key) != delegation["key_id"]:
        raise IdentityError("delegated key_id does not match public key")

    _verify_root_threshold(genesis, delegation, envelope)

    if channel not in delegation["channels"]:
        raise IdentityError(f"channel {channel!r} is outside delegation scope")
    if release_sequence < delegation["release_sequence_min"]:
        raise IdentityError("release sequence is below delegation scope")
    if release_sequence > delegation["release_sequence_max"]:
        raise IdentityError("release sequence is above delegation scope")

    if at.tzinfo is None:
        raise IdentityError("verification time must be timezone-aware")
    check_time = at.astimezone(timezone.utc)
    if check_time < _parse_utc(delegation["valid_from"]):
        raise IdentityError("delegation is not yet valid")
    if check_time >= _parse_utc(delegation["expires"]):
        raise IdentityError("delegation expired")
