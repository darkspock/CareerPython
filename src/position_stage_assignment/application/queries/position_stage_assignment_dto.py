"""Position stage assignment DTOs"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.position_stage_assignment.domain import PositionStageAssignment


@dataclass
class PositionStageAssignmentDto:
    """DTO for position stage assignment"""
    id: str
    position_id: str
    stage_id: str
    assigned_user_ids: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @staticmethod
    def from_entity(entity: PositionStageAssignment) -> 'PositionStageAssignmentDto':
        """Create DTO from entity"""
        return PositionStageAssignmentDto(
            id=entity.id.value,
            position_id=entity.position_id.value,
            stage_id=entity.stage_id.value,
            assigned_user_ids=[uid.value for uid in entity.assigned_user_ids],
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
