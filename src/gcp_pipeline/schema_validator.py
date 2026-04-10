from jsonschema import Draft202012Validator


class SchemaValidator:
    """Wrapper around jsonschema validator."""

    def __init__(self, schema: dict) -> None:
        self._validator = Draft202012Validator(schema)

    def is_valid(self, data: dict) -> bool:
        """Validate a JSON object against the schema."""
        return self._validator.is_valid(data)
