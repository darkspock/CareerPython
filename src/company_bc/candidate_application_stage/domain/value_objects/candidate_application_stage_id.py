"""CandidateStageId value object"""
from dataclasses import dataclass

from src.framework.domain.entities.base import generate_id


@dataclass(frozen=True)
class CandidateApplicationStageId:
    """Value object for candidate stage ID"""
    value: str

    @staticmethod
    def generate() -> 'CandidateApplicationStageId':
        """Generate a new ULID-based ID"""
        return CandidateApplicationStageId(value=generate_id())

    @staticmethod
    def from_string(id_str: str) -> 'CandidateApplicationStageId':
        """Create from string"""
        return CandidateApplicationStageId(value=id_str)

    def __str__(self) -> str:
        return self.value
