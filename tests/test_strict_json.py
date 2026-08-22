from __future__ import annotations

import pytest

from baga_spec.errors import StrictJSONError
from baga_spec.strict_json import loads_strict


def test_parses_ordinary_json() -> None:
    assert loads_strict('{"a":1,"b":[true,null]}') == {"a": 1, "b": [True, None]}


def test_rejects_duplicate_object_keys() -> None:
    with pytest.raises(StrictJSONError, match="duplicate key"):
        loads_strict('{"a":1,"a":2}')


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_rejects_non_finite_numbers(token: str) -> None:
    with pytest.raises(StrictJSONError, match="non-finite"):
        loads_strict('{"value":' + token + '}')


def test_rejects_invalid_utf8_bytes() -> None:
    with pytest.raises(StrictJSONError, match="UTF-8"):
        loads_strict(b'{"x":"\xff"}')
