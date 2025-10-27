"""CandidateStageId value object"""
from dataclasses import dataclass

from src.shared.domain.entities.base import generate_id


@dataclass(frozen=True)
class CandidateStageId:
    """Value object for candidate stage ID"""
    value: str

    @staticmethod
    def generate() -> 'CandidateStageId':
        """Generate a new ULID-based ID"""
        return CandidateStageId(value=generate_id())

    @staticmethod
    def from_string(id_str: str) -> 'CandidateStageId':
        """Create from string"""
        return CandidateStageId(value=id_str)

    def __str__(self) -> str:
        return self.value
