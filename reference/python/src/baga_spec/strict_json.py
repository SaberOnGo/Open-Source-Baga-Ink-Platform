from __future__ import annotations

import json
from typing import Any

from .errors import StrictJSONError

MAX_JSON_BYTES = 1_048_576
MAX_JSON_DEPTH = 64


def _reject_constant(token: str) -> None:
    raise StrictJSONError(
        f"non-finite JSON number is forbidden: {token}",
        code="json_non_finite",
    )


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate key: {key}", code="json_duplicate_key")
        result[key] = value
    return result


def _depth(value: Any, current: int = 0) -> int:
    if isinstance(value, dict):
        if not value:
            return current + 1
        return max(_depth(v, current + 1) for v in value.values())
    if isinstance(value, list):
        if not value:
            return current + 1
        return max(_depth(v, current + 1) for v in value)
    return current


def loads_strict(data: str | bytes) -> Any:
    if isinstance(data, bytes):
        if len(data) > MAX_JSON_BYTES:
            raise StrictJSONError("JSON input too large", code="json_too_large")
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise StrictJSONError("JSON input is not valid UTF-8", code="json_invalid_utf8") from exc
    elif isinstance(data, str):
        try:
            encoded = data.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise StrictJSONError("JSON input contains invalid Unicode", code="json_invalid_unicode") from exc
        if len(encoded) > MAX_JSON_BYTES:
            raise StrictJSONError("JSON input too large", code="json_too_large")
        text = data
    else:
        raise StrictJSONError("JSON input must be str or bytes", code="json_invalid_input_type")

    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_no_duplicates,
            parse_constant=_reject_constant,
        )
    except StrictJSONError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise StrictJSONError(f"invalid JSON: {exc}", code="json_syntax") from exc

    if _depth(value) > MAX_JSON_DEPTH:
        raise StrictJSONError("JSON input too deeply nested", code="json_too_deep")
    return value
