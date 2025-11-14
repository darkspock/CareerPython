"""JobPositionStageId value object"""
from dataclasses import dataclass

from src.framework.domain.entities.base import generate_id


@dataclass(frozen=True)
class JobPositionStageId:
    """Value object for job position stage ID"""
    value: str

    @staticmethod
    def generate() -> 'JobPositionStageId':
        """Generate a new ULID-based ID"""
        return JobPositionStageId(value=generate_id())

    @staticmethod
    def from_string(id_str: str) -> 'JobPositionStageId':
        """Create from string"""
        return JobPositionStageId(value=id_str)

    def __str__(self) -> str:
        return self.value
