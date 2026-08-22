from __future__ import annotations

from datetime import datetime, timezone

import pytest

from baga_spec.errors import IdentityError
from baga_spec.identity import (
    publisher_id,
    verify_app_key_delegation,
    verify_app_ownership,
)

PUBLISHER_ID = "pub1_ofsqstwjfebj4g44rz4fxuo27b3vpnetx2z3uumfpvagrkhups2q"
ROOT_KEY_ID = "ed25519:34750f98bd59fcfc946da45aaabe933be154a4b5094e1c4abf42866505f3c97e"
ROOT_PUBLIC = "iojj3XQJ8ZX9UtstPLpdcspnCb8dlBIb83SIAbQPb1w"
RECOVERY_KEY_ID = "ed25519:6a3803d5f059902a1c6dafbc9ba4729212f7caac08634cc3ae76b27529f03827"
RECOVERY_PUBLIC = "gTl3Dqh9F19Wo1Rmw0x-zMuNipG07jeiXfYPW4_Js5Q"
APP_KEY_ID = "ed25519:b62e867fa2f33afe62d5d6b1642e1621d543307846b2a57b897e710919b76709"
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
    "created_at": "2026-08-22T00:00:00Z",
}
OWNERSHIP_ENVELOPE = {
    "type": "baga.signature-envelope",
    "format": "0.1",
    "signed_type": "baga.app-ownership",
    "signatures": [{
        "key_id": ROOT_KEY_ID,
        "algorithm": "ed25519",
        "signature": "vESfhYCTlHYOQqGMFdR069v2gLmyy2Y-CCn60tEZZxYUSby0JcmcS9ZLbAwxo0eUVrRxAcHeb7DYgiMsnzNSCw",
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
    "channels": ["stable"],
    "release_sequence_min": 1,
    "release_sequence_max": 100,
    "valid_from": "2026-08-22T00:00:00Z",
    "expires": "2027-08-22T00:00:00Z",
}
DELEGATION_ENVELOPE = {
    "type": "baga.signature-envelope",
    "format": "0.1",
    "signed_type": "baga.app-key-delegation",
    "signatures": [{
        "key_id": ROOT_KEY_ID,
        "algorithm": "ed25519",
        "signature": "zgwA4KfKvpCqQmc7MEkSvTf9T5fhq7aIwdzIgNZQlsKIECYfn2i5PrRHhn3xrlLn1qPRRPDR4mIOY43a83rACQ",
    }],
}


def test_publisher_id_matches_fixed_genesis_vector() -> None:
    assert publisher_id(GENESIS) == PUBLISHER_ID


def test_root_signed_app_ownership_is_accepted() -> None:
    verify_app_ownership(GENESIS, OWNERSHIP, OWNERSHIP_ENVELOPE)


def test_root_signed_delegation_is_accepted_for_scope() -> None:
    verify_app_key_delegation(
        GENESIS,
        DELEGATION,
        DELEGATION_ENVELOPE,
        app_id="com.example.reader",
        channel="stable",
        release_sequence=1,
        at=datetime(2026, 8, 23, tzinfo=timezone.utc),
    )


def test_delegation_rejects_wrong_channel() -> None:
    with pytest.raises(IdentityError, match="channel"):
        verify_app_key_delegation(
            GENESIS,
            DELEGATION,
            DELEGATION_ENVELOPE,
            app_id="com.example.reader",
            channel="beta",
            release_sequence=1,
            at=datetime(2026, 8, 23, tzinfo=timezone.utc),
        )


def test_delegation_rejects_expired_time() -> None:
    with pytest.raises(IdentityError, match="expired"):
        verify_app_key_delegation(
            GENESIS,
            DELEGATION,
            DELEGATION_ENVELOPE,
            app_id="com.example.reader",
            channel="stable",
            release_sequence=1,
            at=datetime(2028, 1, 1, tzinfo=timezone.utc),
        )
