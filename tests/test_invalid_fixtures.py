from __future__ import annotations

import json
import warnings
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from baga_spec.errors import BagaSpecError
from baga_spec.ikp import verify_ikp
from baga_spec.schemas import validate_schema
from baga_spec.strict_json import loads_strict

ROOT = Path(__file__).resolve().parents[1]
INVALID_ROOT = ROOT / "spec" / "fixtures" / "invalid"


def _generated_bad_ikp(path: Path, mutation: str) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            if mutation == "path-traversal":
                archive.writestr("../escape", b"bad")
            elif mutation == "duplicate-entry":
                archive.writestr("main.lua", b"one")
                archive.writestr("main.lua", b"two")
            else:
                raise AssertionError(f"unknown invalid fixture mutation: {mutation}")


def test_every_invalid_fixture_is_rejected_with_expected_machine_code(tmp_path: Path) -> None:
    manifest = json.loads((INVALID_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["cases"], "invalid corpus must not be empty"

    for case in manifest["cases"]:
        with pytest.raises(BagaSpecError) as raised:
            if case["kind"] == "strict-json":
                loads_strict((INVALID_ROOT / case["path"]).read_bytes())
            elif case["kind"] == "schema":
                instance = loads_strict((INVALID_ROOT / case["path"]).read_bytes())
                validate_schema(case["schema"], instance)
            elif case["kind"] == "generated-ikp":
                ikp = tmp_path / f"{case['id']}.ikp"
                _generated_bad_ikp(ikp, case["mutation"])
                verify_ikp(ikp, at=datetime(2026, 8, 23, tzinfo=timezone.utc))
            else:
                raise AssertionError(f"unknown invalid fixture kind: {case['kind']}")
        assert raised.value.code == case["expected_error_code"], case["id"]
