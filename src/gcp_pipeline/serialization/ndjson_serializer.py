import json
from typing import Any, Iterable, Protocol


class DataSerializer(Protocol):
    """"""

    def write(self, data: Iterable[Any]) -> Any: ...

    def read(self, data: str) -> list[Any]: ...


class NDJSONSerializer:
    """"""

    def write(self, data: Iterable[dict]) -> str:
        """"""
        return "\n".join(json.dumps(record) for record in data)

    def read(self, data: str) -> list[dict]:
        return [json.loads(line) for line in data.splitlines() if line.strip()]
