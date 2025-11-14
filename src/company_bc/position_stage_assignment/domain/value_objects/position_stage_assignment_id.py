"""Position stage assignment ID value object"""
from dataclasses import dataclass

import ulid


@dataclass(frozen=True)
class PositionStageAssignmentId:
    """Value object for position stage assignment ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Position stage assignment ID cannot be empty")

    @staticmethod
    def generate() -> 'PositionStageAssignmentId':
        """Generate a new unique position stage assignment ID"""
        return PositionStageAssignmentId(value=str(ulid.new()))

    @staticmethod
    def from_string(value: str) -> 'PositionStageAssignmentId':
        """Create from string"""
        return PositionStageAssignmentId(value=value)

    def __str__(self) -> str:
        return self.value
