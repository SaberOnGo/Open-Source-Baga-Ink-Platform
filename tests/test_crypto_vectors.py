from __future__ import annotations

import base64

import pytest

from baga_spec.crypto import (
    ed25519_key_id,
    ed25519_public_key_from_seed,
    sign_ed25519,
    verify_ed25519,
)
from baga_spec.errors import SignatureError

ROOT_SEED = bytes.fromhex("01" * 32)
ROOT_PUBLIC_B64 = "iojj3XQJ8ZX9UtstPLpdcspnCb8dlBIb83SIAbQPb1w"
ROOT_KEY_ID = "ed25519:NHUPmL1Z_PyUbaRaqr6TO-FUpLUJThxKv0KGZQXzyX4"
OWNERSHIP_CANONICAL = b'{"app_id":"com.example.reader","created_at":"2026-08-22T00:00:00Z","format":"0.1","ownership_sequence":1,"publisher_id":"pub1_fy3xxqegf6r7ns6e3x3nuxhcqvpcrrn3nue72jvfmzhf6c2kutmq","status":"active","type":"baga.app-ownership"}'
OWNERSHIP_SIGNATURE_B64 = "xo_3WL2fzimT8pCNgprNGbnBzVQL0dR0Tv-8bilETeBqBYm2PUGutt_2L55I6G9A8gYAHhrYyWCua6xWGlkMCg"


def _b64u_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def test_fixed_seed_produces_expected_public_key_and_key_id() -> None:
    public_key = ed25519_public_key_from_seed(ROOT_SEED)
    assert public_key == _b64u_decode(ROOT_PUBLIC_B64)
    assert ed25519_key_id(public_key) == ROOT_KEY_ID


def test_fixed_signature_vector_is_stable() -> None:
    signature = sign_ed25519(ROOT_SEED, OWNERSHIP_CANONICAL)
    assert signature == _b64u_decode(OWNERSHIP_SIGNATURE_B64)
    verify_ed25519(_b64u_decode(ROOT_PUBLIC_B64), OWNERSHIP_CANONICAL, signature)


def test_modified_message_is_rejected() -> None:
    with pytest.raises(SignatureError):
        verify_ed25519(
            _b64u_decode(ROOT_PUBLIC_B64),
            OWNERSHIP_CANONICAL + b" ",
            _b64u_decode(OWNERSHIP_SIGNATURE_B64),
        )
