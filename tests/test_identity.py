from __future__ import annotations

from datetime import datetime, timezone

import pytest

from baga_spec.errors import IdentityError
from baga_spec.identity import publisher_id, verify_app_key_delegation, verify_app_ownership

PUBLISHER_ID = "pub1_fy3xxqegf6r7ns6e3x3nuxhcqvpcrrn3nue72jvfmzhf6c2kutmq"
ROOT_KEY_ID = "ed25519:NHUPmL1Z_PyUbaRaqr6TO-FUpLUJThxKv0KGZQXzyX4"
ROOT_PUBLIC = "iojj3XQJ8ZX9UtstPLpdcspnCb8dlBIb83SIAbQPb1w"
RECOVERY_KEY_ID = "ed25519:ajgD1fBZkCocba-8m6RykhL3yqwIY0zDrnaydSnwOCc"
RECOVERY_PUBLIC = "gTl3Dqh9F19Wo1Rmw0x-zMuNipG07jeiXfYPW4_Js5Q"
APP_KEY_ID = "ed25519:ti6Gf6LzOv5i1daxZC4WIdVDMHhGsqV7iX5xCRm3Zwk"
APP_PUBLIC = "7UkoxijRwsbq6QM4kFmVYSlZJzpcY_k2NsFGFKyHN9E"

GENESIS = {
    "type": "baga.publisher-genesis",
    "format": "0.1",
    "display_name": "Example Studio",
    "root_threshold": 1,
    "root_keys": [{"key_id": ROOT_KEY_ID, "algorithm": "ed25519", "public_key": ROOT_PUBLIC}],
    "recovery_threshold": 1,
    "recovery_keys": [{"key_id": RECOVERY_KEY_ID, "algorithm": "ed25519", "public_key": RECOVERY_PUBLIC}],
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
OWNERSHIP_SIGNATURES = {
    "type": "baga.signature-set",
    "format": "0.1",
    "signed_object": "app-ownership.json",
    "signed_object_sha256": "sha256:5bbdceadb99b72e443d6093e3b0835ac8c4d45844b9c0e7751d989df412962b9",
    "signatures": [{
        "key_id": ROOT_KEY_ID,
        "algorithm": "ed25519",
        "signature": "xo_3WL2fzimT8pCNgprNGbnBzVQL0dR0Tv-8bilETeBqBYm2PUGutt_2L55I6G9A8gYAHhrYyWCua6xWGlkMCg",
    }],
}
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
DELEGATION_SIGNATURES = {
    "type": "baga.signature-set",
    "format": "0.1",
    "signed_object": "app-key-delegation.json",
    "signed_object_sha256": "sha256:9295d432e12360c1f4467c2d8304c2f340f7ff247c3eecd27630b0d31d30bfdb",
    "signatures": [{
        "key_id": ROOT_KEY_ID,
        "algorithm": "ed25519",
        "signature": "iS_9qeKI79WWrzLXvH7drk_ARrkXYZuMK6RDizTVuDIkXylajiS4kC7wIFyMK4tECGgJxeE1Kv5vcoWpC3znDQ",
    }],
}


def test_publisher_id_matches_fixed_genesis_vector() -> None:
    assert publisher_id(GENESIS) == PUBLISHER_ID


def test_root_signed_app_ownership_is_accepted() -> None:
    verify_app_ownership(GENESIS, OWNERSHIP, OWNERSHIP_SIGNATURES)


def test_root_signed_delegation_is_accepted_for_scope() -> None:
    verify_app_key_delegation(
        GENESIS, DELEGATION, DELEGATION_SIGNATURES,
        app_id="com.example.reader", channel="stable", release_sequence=1,
        at=datetime(2026, 8, 23, tzinfo=timezone.utc),
    )


def test_delegation_rejects_wrong_channel() -> None:
    with pytest.raises(IdentityError, match="channel"):
        verify_app_key_delegation(
            GENESIS, DELEGATION, DELEGATION_SIGNATURES,
            app_id="com.example.reader", channel="beta", release_sequence=1,
            at=datetime(2026, 8, 23, tzinfo=timezone.utc),
        )


def test_delegation_rejects_expired_time() -> None:
    with pytest.raises(IdentityError, match="expired"):
        verify_app_key_delegation(
            GENESIS, DELEGATION, DELEGATION_SIGNATURES,
            app_id="com.example.reader", channel="stable", release_sequence=1,
            at=datetime(2028, 1, 1, tzinfo=timezone.utc),
        )
