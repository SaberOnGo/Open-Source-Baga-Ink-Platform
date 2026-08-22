from __future__ import annotations

import stat
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath

from .canonical import canonical_sha256
from .crypto import sha256_digest
from .errors import IKPError, BagaSpecError
from .identity import publisher_id, verify_app_key_delegation, verify_app_ownership
from .schemas import validate_schema
from .signing import verify_release_statement
from .strict_json import loads_strict


@dataclass(frozen=True)
class IKPLimits:
    max_container_bytes: int = 64 * 1024 * 1024
    max_uncompressed_bytes: int = 128 * 1024 * 1024
    max_file_bytes: int = 32 * 1024 * 1024
    max_entries: int = 4096
    max_compression_ratio: int = 200


DEFAULT_LIMITS = IKPLimits()


@dataclass(frozen=True)
class VerifiedIKP:
    app_id: str
    publisher_id: str
    version_name: str
    release_sequence: int
    channel: str
    package_sha256: str
    package_length: int


_REQUIRED_SIGNATURE_FILES = {
    "signature/files.json",
    "signature/publisher-genesis.json",
    "signature/app-ownership.json",
    "signature/app-ownership.signatures.json",
    "signature/app-key-delegation.json",
    "signature/app-key-delegation.signatures.json",
    "signature/release-statement.json",
    "signature/release.signatures.json",
}

_FORBIDDEN_NATIVE_SUFFIXES = {
    ".so", ".dll", ".dylib", ".dex", ".jar", ".apk", ".exe",
}


def _safe_path(name: str) -> bool:
    if not name or "\\" in name:
        return False
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        return False
    return all(part not in ("", ".") for part in path.parts)


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_IFMT(mode) == stat.S_IFLNK


def _read_json(entries: dict[str, bytes], path: str, schema: str | None = None) -> dict:
    if path not in entries:
        raise IKPError(f"missing required IKP file: {path}")
    try:
        value = loads_strict(entries[path])
        if not isinstance(value, dict):
            raise IKPError(f"{path} must contain a JSON object")
        if schema is not None:
            validate_schema(schema, value)
        return value
    except BagaSpecError as exc:
        if isinstance(exc, IKPError):
            raise
        raise IKPError(f"invalid {path}: {exc}") from exc


def _verify_target_bytes(target: dict, expected_path: str, data: bytes, label: str) -> None:
    if target["path"] != expected_path:
        raise IKPError(f"{label} path mismatch")
    if target["length"] != len(data):
        raise IKPError(f"{label} length mismatch")
    if target["sha256"] != sha256_digest(data):
        raise IKPError(f"{label} hash mismatch")


def _validate_payload_manifest(entries: dict[str, bytes], files_manifest: dict) -> None:
    payload_paths = sorted(
        (path for path in entries if not path.startswith("signature/")),
        key=lambda value: value.encode("utf-8"),
    )
    listed = files_manifest["files"]
    listed_paths = [item["path"] for item in listed]
    if listed_paths != sorted(listed_paths, key=lambda value: value.encode("utf-8")):
        raise IKPError("payload files manifest is not sorted by UTF-8 path bytes")
    if len(listed_paths) != len(set(listed_paths)):
        raise IKPError("payload files manifest contains duplicate paths")
    if listed_paths != payload_paths:
        raise IKPError("payload files manifest does not exactly match IKP payload")
    for item in listed:
        data = entries[item["path"]]
        if item["length"] != len(data) or item["sha256"] != sha256_digest(data):
            raise IKPError(f"payload integrity mismatch: {item['path']}")


def _reject_native_payload(entries: dict[str, bytes]) -> None:
    for path, data in entries.items():
        if path.startswith("signature/"):
            continue
        suffix = PurePosixPath(path).suffix.lower()
        if suffix in _FORBIDDEN_NATIVE_SUFFIXES or data.startswith(b"\x7fELF"):
            raise IKPError(f"native executable dependency is forbidden in Universal IKP: {path}")


def _read_zip(path: Path, limits: IKPLimits) -> dict[str, bytes]:
    try:
        container_size = path.stat().st_size
    except OSError as exc:
        raise IKPError(f"cannot stat IKP: {exc}") from exc
    if container_size > limits.max_container_bytes:
        raise IKPError("IKP container exceeds size limit")

    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = archive.infolist()
            if len(infos) > limits.max_entries:
                raise IKPError("IKP contains too many ZIP entries")
            names: set[str] = set()
            total_uncompressed = 0
            entries: dict[str, bytes] = {}
            for info in infos:
                name = info.filename
                if name in names:
                    raise IKPError(f"duplicate ZIP entry: {name}")
                names.add(name)
                if not _safe_path(name):
                    raise IKPError(f"unsafe ZIP path: {name}")
                if info.is_dir():
                    continue
                if _is_symlink(info):
                    raise IKPError(f"symbolic links are forbidden in IKP: {name}")
                if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise IKPError(f"unsupported ZIP compression method for {name}")
                if info.file_size > limits.max_file_bytes:
                    raise IKPError(f"IKP file exceeds size limit: {name}")
                total_uncompressed += info.file_size
                if total_uncompressed > limits.max_uncompressed_bytes:
                    raise IKPError("IKP uncompressed size exceeds limit")
                if info.file_size and info.compress_size == 0:
                    raise IKPError(f"invalid compressed size for {name}")
                if info.compress_size and info.file_size / info.compress_size > limits.max_compression_ratio:
                    raise IKPError(f"IKP compression ratio exceeds limit: {name}")
                data = archive.read(info)
                if len(data) != info.file_size:
                    raise IKPError(f"ZIP entry length changed while reading: {name}")
                entries[name] = data
            return entries
    except zipfile.BadZipFile as exc:
        raise IKPError("invalid IKP ZIP container") from exc


def verify_ikp(path: Path, *, at: datetime, limits: IKPLimits = DEFAULT_LIMITS) -> VerifiedIKP:
    entries = _read_zip(path, limits)
    if "manifest.json" not in entries:
        raise IKPError("missing manifest.json")
    missing_signature = sorted(_REQUIRED_SIGNATURE_FILES.difference(entries))
    if missing_signature:
        raise IKPError("missing signature evidence: " + ", ".join(missing_signature))

    manifest = _read_json(entries, "manifest.json", "ikp-manifest")
    files_manifest = _read_json(entries, "signature/files.json", "files-manifest")
    genesis = _read_json(entries, "signature/publisher-genesis.json", "publisher-genesis")
    ownership = _read_json(entries, "signature/app-ownership.json", "app-ownership")
    ownership_signatures = _read_json(entries, "signature/app-ownership.signatures.json", "signature-set")
    delegation = _read_json(entries, "signature/app-key-delegation.json", "app-key-delegation")
    delegation_signatures = _read_json(entries, "signature/app-key-delegation.signatures.json", "signature-set")
    release = _read_json(entries, "signature/release-statement.json", "ikp-release")
    release_signatures = _read_json(entries, "signature/release.signatures.json", "signature-set")

    _validate_payload_manifest(entries, files_manifest)
    _reject_native_payload(entries)

    entry = manifest["entry"]
    if not _safe_path(entry) or entry.startswith("signature/") or entry not in entries:
        raise IKPError("manifest entry point is missing or unsafe")

    expected_publisher = publisher_id(genesis)
    if release["publisher_id"] != expected_publisher:
        raise IKPError("release publisher_id does not match Publisher Genesis")
    if ownership["app_id"] != manifest["id"] or delegation["app_id"] != manifest["id"]:
        raise IKPError("identity app_id does not match manifest")

    try:
        verify_app_ownership(genesis, ownership, ownership_signatures)
        verify_app_key_delegation(
            genesis,
            delegation,
            delegation_signatures,
            app_id=manifest["id"],
            channel=release["channel"],
            release_sequence=release["release_sequence"],
            at=at,
        )
        verify_release_statement(release, release_signatures, delegation, at=at)
    except BagaSpecError as exc:
        raise IKPError(f"publisher signature chain invalid: {exc}") from exc

    _verify_target_bytes(release["manifest"], "manifest.json", entries["manifest.json"], "manifest")
    _verify_target_bytes(release["files_manifest"], "signature/files.json", entries["signature/files.json"], "files manifest")
    if release["publisher_identity_digest"] != canonical_sha256(genesis):
        raise IKPError("Publisher Identity digest mismatch")
    if release["app_ownership_digest"] != canonical_sha256(ownership):
        raise IKPError("App Ownership digest mismatch")
    if release["app_key_delegation_digest"] != canonical_sha256(delegation):
        raise IKPError("App Key Delegation digest mismatch")

    comparisons = {
        "app_id": (release["app_id"], manifest["id"]),
        "version_name": (release["version_name"], manifest["version_name"]),
        "release_sequence": (release["release_sequence"], manifest["release_sequence"]),
        "channel": (release["channel"], manifest["channel"]),
        "ikp_format": (release["ikp_format"], manifest["ikp_format"]),
        "baga_api": (release["baga_api"], manifest["baga_api"]),
    }
    for field, (signed_value, manifest_value) in comparisons.items():
        if signed_value != manifest_value:
            raise IKPError(f"release/manifest {field} mismatch")

    package_bytes = path.read_bytes()
    return VerifiedIKP(
        app_id=manifest["id"],
        publisher_id=expected_publisher,
        version_name=manifest["version_name"],
        release_sequence=manifest["release_sequence"],
        channel=manifest["channel"],
        package_sha256=sha256_digest(package_bytes),
        package_length=len(package_bytes),
    )
