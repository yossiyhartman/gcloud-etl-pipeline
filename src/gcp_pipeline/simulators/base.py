from dataclasses import dataclass
from typing import Any, Protocol

# @dataclass
# class Person:
#     name: str


# @dataclass
# class Group:
#     group: list[Person]


class DataGenerator(Protocol):
    """The protocol to which all data generator classes adhere."""

    def generate(self, n_days: int) -> list[Any]:
        """
        Generate data for `n` days

        Arguments
            n_days (int) create for `n` days data
        """
        ...
