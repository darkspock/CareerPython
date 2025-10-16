from dataclasses import dataclass
from typing import Any

import ulid


@dataclass(frozen=True)
class JobPositionId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("JobPositionId cannot be empty")

    @classmethod
    def generate(cls) -> 'JobPositionId':
        """Generate a new JobPositionId using ULID"""
        return cls(ulid.new().str)

    @classmethod
    def from_string(cls, id_str: str) -> 'JobPositionId':
        """Create JobPositionId from string"""
        if not id_str:
            raise ValueError("ID string cannot be empty")
        return cls(id_str)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, JobPositionId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
