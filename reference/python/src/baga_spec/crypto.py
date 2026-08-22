from __future__ import annotations

import base64
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .errors import SignatureError


def b64u_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64u_decode(value: str) -> bytes:
    try:
        decoded = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except Exception as exc:
        raise SignatureError("invalid base64url value") from exc
    if b64u_encode(decoded) != value:
        raise SignatureError("base64url value is not canonical unpadded encoding")
    return decoded


def sha256_digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def ed25519_public_key_from_seed(seed32: bytes) -> bytes:
    if len(seed32) != 32:
        raise SignatureError("Ed25519 seed must be exactly 32 bytes")
    private_key = Ed25519PrivateKey.from_private_bytes(seed32)
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def ed25519_key_id(public_key: bytes) -> str:
    if len(public_key) != 32:
        raise SignatureError("Ed25519 public key must be exactly 32 bytes")
    return "ed25519:" + b64u_encode(hashlib.sha256(public_key).digest())


def sign_ed25519(seed32: bytes, message: bytes) -> bytes:
    if len(seed32) != 32:
        raise SignatureError("Ed25519 seed must be exactly 32 bytes")
    return Ed25519PrivateKey.from_private_bytes(seed32).sign(message)


def verify_ed25519(public_key: bytes, message: bytes, signature: bytes) -> None:
    if len(public_key) != 32:
        raise SignatureError("Ed25519 public key must be exactly 32 bytes")
    if len(signature) != 64:
        raise SignatureError("Ed25519 signature must be exactly 64 bytes")
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature, message)
    except (InvalidSignature, ValueError) as exc:
        raise SignatureError("invalid Ed25519 signature") from exc
