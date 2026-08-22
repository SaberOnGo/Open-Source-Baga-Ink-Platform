from __future__ import annotations


class BagaSpecError(ValueError):
    """Base error for executable specification validation failures."""

    code = "baga_spec_error"


class StrictJSONError(BagaSpecError):
    code = "strict_json_error"


class SchemaValidationError(BagaSpecError):
    code = "schema_validation_error"


class SignatureError(BagaSpecError):
    code = "signature_error"


class IdentityError(BagaSpecError):
    code = "identity_error"


class IKPError(BagaSpecError):
    code = "ikp_error"
