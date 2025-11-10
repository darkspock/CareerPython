"""Job Position Comment DTO."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JobPositionCommentDto:
    """
    Data Transfer Object for JobPositionComment
    Used to transfer comment data between layers
    """
    id: str
    job_position_id: str
    comment: str
    workflow_id: Optional[str]
    stage_id: Optional[str]  # NULL = global comment
    created_by_user_id: str
    review_status: str
    visibility: str
    created_at: datetime
    updated_at: datetime
    is_global: bool

    @staticmethod
    def from_entity(entity) -> "JobPositionCommentDto":  # type: ignore
        """
        Convert domain entity to DTO
        
        Args:
            entity: JobPositionComment entity
            
        Returns:
            JobPositionCommentDto
        """
        return JobPositionCommentDto(
            id=str(entity.id),
            job_position_id=str(entity.job_position_id),
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=entity.stage_id,
            created_by_user_id=str(entity.created_by_user_id),
            review_status=entity.review_status.value,
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_global=entity.is_global,
        )

