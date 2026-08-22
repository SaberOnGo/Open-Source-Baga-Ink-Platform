from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import SchemaValidationError

_REPO_ROOT = Path(__file__).resolve().parents[4]
_SCHEMA_ROOT = _REPO_ROOT / "spec" / "schemas"


@lru_cache(maxsize=None)
def schema_path(name: str) -> Path:
    matches = list(_SCHEMA_ROOT.rglob(f"{name}.schema.json"))
    if len(matches) != 1:
        raise SchemaValidationError(
            f"schema {name!r} must resolve to exactly one file, found {len(matches)}"
        )
    return matches[0]


@lru_cache(maxsize=None)
def _load_schema(name: str) -> dict[str, Any]:
    path = schema_path(name)
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        raise SchemaValidationError(f"invalid schema {name}: {exc}") from exc
    return schema


def validate_schema(name: str, instance: Any) -> None:
    validator = Draft202012Validator(_load_schema(name))
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    if not errors:
        return
    error: ValidationError = errors[0]
    location = ".".join(str(part) for part in error.absolute_path)
    prefix = f"{location}: " if location else ""
    raise SchemaValidationError(prefix + error.message)
