import json

import pytest

from gcp_pipeline.serialization import NDJSONSerializer


@pytest.fixture
def serializer():
    return NDJSONSerializer()


def test_write_basic(serializer):
    data = [{"a": 1}, {"b": 2}]
    result = serializer.write(data)

    expected = "\n".join(json.dumps(d) for d in data)
    assert result == expected


def test_write_empty(serializer):
    assert serializer.write([]) == ""


def test_read_basic(serializer):
    data = [{"a": 1}, {"b": 2}]
    ndjson = "\n".join(json.dumps(d) for d in data)

    result = serializer.read(ndjson)
    assert result == data


def test_read_ignores_empty_lines(serializer):
    ndjson = '{"a": 1}\n\n  \n{"b": 2}\n'
    result = serializer.read(ndjson)

    assert result == [{"a": 1}, {"b": 2}]


def test_round_trip(serializer):
    data = [{"x": 10}, {"y": [1, 2, 3]}, {"z": {"nested": True}}]

    written = serializer.write(data)
    read_back = serializer.read(written)

    assert read_back == data


def test_read_invalid_json(serializer):
    ndjson = '{"a": 1}\nINVALID_JSON\n{"b": 2}'

    with pytest.raises(json.JSONDecodeError):
        serializer.read(ndjson)


def test_write_preserves_order(serializer):
    data = [{"a": 1}, {"b": 2}, {"c": 3}]
    result = serializer.write(data)

    lines = result.splitlines()
    parsed = [json.loads(line) for line in lines]

    assert parsed == data
