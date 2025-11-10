"""Phase ID value object"""
from dataclasses import dataclass

from src.framework.domain.entities.base import generate_id


@dataclass(frozen=True)
class PhaseId:
    """Phase identifier value object"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("PhaseId cannot be empty")

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def generate() -> 'PhaseId':
        """Generate a new PhaseId"""
        return PhaseId(generate_id())

    @staticmethod
    def from_string(value: str) -> 'PhaseId':
        """Create PhaseId from string"""
        return PhaseId(value)
