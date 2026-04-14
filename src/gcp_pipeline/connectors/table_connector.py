from typing import Any, Protocol

import polars as pl


class TableStorageConnector(Protocol):
    """"""

    def write(self, path: str, data: Any) -> None:
        """"""
        ...

    def read(self, path: str) -> Any:
        """"""
        ...


class DeltaStorageConnector:
    def read(self, path: str) -> pl.DataFrame:
        """"""
        return pl.read_delta(path)

    def write(self, path: str, data: pl.DataFrame) -> None:
        """"""
        data.write_delta(path, mode="overwrite")
