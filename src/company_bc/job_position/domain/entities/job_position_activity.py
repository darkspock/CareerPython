"""Job Position Activity Entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from src.company_bc.job_position.domain.value_objects import (
    JobPositionActivityId,
    JobPositionId,
)
from src.company_bc.job_position.domain.enums.activity_type_enum import ActivityTypeEnum
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId


@dataclass
class JobPositionActivity:
    """
    JobPositionActivity domain entity
    Represents an activity/interaction on a job position
    
    Activities track the history of changes and interactions:
    - CREATED: Position was created
    - EDITED: Fields were modified
    - STAGE_MOVED: Position moved to a different stage
    - STATUS_CHANGED: Status was changed (draft → active, etc.)
    - COMMENT_ADDED: Comment was added to the position
    """
    id: JobPositionActivityId
    job_position_id: JobPositionId
    activity_type: ActivityTypeEnum
    description: str
    performed_by_user_id: CompanyUserId
    metadata: Dict[str, Any]
    created_at: datetime

    @classmethod
    def create(
        cls,
        id: JobPositionActivityId,
        job_position_id: JobPositionId,
        activity_type: ActivityTypeEnum,
        description: str,
        performed_by_user_id: CompanyUserId,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "JobPositionActivity":
        """
        Factory method to create a new activity

        Args:
            id: Activity ID (required, must be provided from outside)
            job_position_id: JobPosition ID this activity belongs to
            activity_type: Type of activity
            description: Human-readable description of the activity
            performed_by_user_id: User who performed this activity
            metadata: Additional data about the activity (optional)

        Returns:
            JobPositionActivity: New activity instance
        """
        return cls(
            id=id,
            job_position_id=job_position_id,
            activity_type=activity_type,
            description=description,
            performed_by_user_id=performed_by_user_id,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )

    @staticmethod
    def from_edit(
        id: JobPositionActivityId,
        job_position_id: JobPositionId,
        user_id: CompanyUserId,
        changed_fields: list[str],
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
    ) -> "JobPositionActivity":
        """
        Static factory to create an EDITED activity

        Args:
            id: Activity ID
            job_position_id: JobPosition ID
            user_id: User who performed the edit
            changed_fields: List of field names that were changed
            old_values: Dict of old values {field_name: old_value}
            new_values: Dict of new values {field_name: new_value}

        Returns:
            JobPositionActivity: Activity for the edit
        """
        description = f"Edited fields: {', '.join(changed_fields)}"
        metadata = {
            "changed_fields": changed_fields,
            "old_values": old_values,
            "new_values": new_values,
        }
        
        return JobPositionActivity.create(
            id=id,
            job_position_id=job_position_id,
            activity_type=ActivityTypeEnum.EDITED,
            description=description,
            performed_by_user_id=user_id,
            metadata=metadata,
        )

    @staticmethod
    def from_stage_move(
        id: JobPositionActivityId,
        job_position_id: JobPositionId,
        user_id: CompanyUserId,
        old_stage_id: Optional[str],
        old_stage_name: Optional[str],
        new_stage_id: str,
        new_stage_name: str,
    ) -> "JobPositionActivity":
        """
        Static factory to create a STAGE_MOVED activity

        Args:
            id: Activity ID
            job_position_id: JobPosition ID
            user_id: User who moved the stage
            old_stage_id: Previous stage ID (can be None for new positions)
            old_stage_name: Previous stage name
            new_stage_id: New stage ID
            new_stage_name: New stage name

        Returns:
            JobPositionActivity: Activity for the stage move
        """
        if old_stage_name:
            description = f"Moved from '{old_stage_name}' to '{new_stage_name}'"
        else:
            description = f"Moved to '{new_stage_name}'"
            
        metadata = {
            "old_stage_id": old_stage_id,
            "old_stage_name": old_stage_name,
            "new_stage_id": new_stage_id,
            "new_stage_name": new_stage_name,
        }
        
        return JobPositionActivity.create(
            id=id,
            job_position_id=job_position_id,
            activity_type=ActivityTypeEnum.STAGE_MOVED,
            description=description,
            performed_by_user_id=user_id,
            metadata=metadata,
        )

    @staticmethod
    def from_status_change(
        id: JobPositionActivityId,
        job_position_id: JobPositionId,
        user_id: CompanyUserId,
        old_status: str,
        new_status: str,
    ) -> "JobPositionActivity":
        """
        Static factory to create a STATUS_CHANGED activity

        Args:
            id: Activity ID
            job_position_id: JobPosition ID
            user_id: User who changed the status
            old_status: Previous status
            new_status: New status

        Returns:
            JobPositionActivity: Activity for the status change
        """
        description = f"Status changed from '{old_status}' to '{new_status}'"
        metadata = {
            "old_status": old_status,
            "new_status": new_status,
        }
        
        return JobPositionActivity.create(
            id=id,
            job_position_id=job_position_id,
            activity_type=ActivityTypeEnum.STATUS_CHANGED,
            description=description,
            performed_by_user_id=user_id,
            metadata=metadata,
        )

    @staticmethod
    def from_comment_added(
        id: JobPositionActivityId,
        job_position_id: JobPositionId,
        user_id: CompanyUserId,
        comment_id: str,
        is_global: bool,
    ) -> "JobPositionActivity":
        """
        Static factory to create a COMMENT_ADDED activity

        Args:
            id: Activity ID
            job_position_id: JobPosition ID
            user_id: User who added the comment
            comment_id: ID of the added comment
            is_global: Whether this is a global comment

        Returns:
            JobPositionActivity: Activity for the comment addition
        """
        description = f"Added a {'global ' if is_global else ''}comment"
        metadata = {
            "comment_id": comment_id,
            "is_global": is_global,
        }
        
        return JobPositionActivity.create(
            id=id,
            job_position_id=job_position_id,
            activity_type=ActivityTypeEnum.COMMENT_ADDED,
            description=description,
            performed_by_user_id=user_id,
            metadata=metadata,
        )

