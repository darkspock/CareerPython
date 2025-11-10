from abc import ABC
from dataclasses import dataclass
from typing import Any, TypeVar, Type

import ulid

T = TypeVar('T', bound='BaseId')


@dataclass(frozen=True)
class BaseId(ABC):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError(f"{self.__class__.__name__} cannot be empty")

    @classmethod
    def generate(cls: Type[T]) -> T:
        """Generate a new ID using ULID"""
        return cls(ulid.new().str)

    @classmethod
    def from_string(cls: Type[T], id_str: str) -> T:
        """Create ID from string"""
        if not id_str:
            raise ValueError("ID string cannot be empty")
        return cls(id_str)

    @classmethod
    def from_string_or_null(cls: Type[T], id_str: str | None) -> T | None:
        """Create ID from string"""
        if not id_str:
            return None
        return cls(id_str)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
