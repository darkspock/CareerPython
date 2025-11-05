"""Job Position Activity DTO."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class JobPositionActivityDto:
    """
    Data Transfer Object for JobPositionActivity
    Used to transfer activity data between layers
    """
    id: str
    job_position_id: str
    activity_type: str
    description: str
    performed_by_user_id: str
    metadata: Dict[str, Any]
    created_at: datetime

    @staticmethod
    def from_entity(entity) -> "JobPositionActivityDto":  # type: ignore
        """
        Convert domain entity to DTO
        
        Args:
            entity: JobPositionActivity entity
            
        Returns:
            JobPositionActivityDto
        """
        return JobPositionActivityDto(
            id=str(entity.id),
            job_position_id=str(entity.job_position_id),
            activity_type=entity.activity_type.value,
            description=entity.description,
            performed_by_user_id=str(entity.performed_by_user_id),
            metadata=entity.metadata,
            created_at=entity.created_at,
        )

