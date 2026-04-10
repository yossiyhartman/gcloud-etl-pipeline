from pytest import fixture

from gcp_pipeline.schema_validator import SchemaValidator


@fixture
def expected_schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "mood.schema",
        "title": "Mood",
        "description": "Measured mood on a given day",
        "type": "object",
        "properties": {"event_time": {"type": "string"}, "name": {"type": "string"}, "mood": {"type": "string"}},
        "required": ["event_time", "name", "mood"],
        "additionalProperties": False,
    }


class TestSchema:
    def test_valid_data(self, expected_schema):
        sample_data = {"event_time": "2000-02-10", "name": "john", "mood": "moody"}
        validator = SchemaValidator(schema=expected_schema)

        result = validator.is_valid(sample_data)

        assert result

    def test_invalid_data(self, expected_schema):
        sample_data = {"event_time": "2000-02-10", "name": 0, "mood": ["moody", "happy"]}
        validator = SchemaValidator(schema=expected_schema)

        result = validator.is_valid(sample_data)

        assert not result
