from typing import Any, Protocol


class DataGenerator(Protocol):
    """The protocol to which all data generator classes adhere."""

    def generate(self, n_records: int) -> list[Any]:
        """
        Generate `n` amount of records
        """
        ...
