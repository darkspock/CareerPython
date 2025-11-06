"""
Task DTO Mapper
Phase 6: Mapper to convert CandidateApplication entity to enriched TaskDto
"""

from typing import Optional

from src.candidate_application.application.queries.shared.task_dto import TaskDto
from src.candidate_application.domain.entities.candidate_application import CandidateApplication


class TaskDtoMapper:
    """Mapper for converting entities to TaskDto with enriched information"""

    @staticmethod
    def from_entity(
            application: CandidateApplication,
            candidate_name: str,
            position_title: str,
            current_stage_name: Optional[str] = None,
            candidate_email: Optional[str] = None,
            candidate_photo_url: Optional[str] = None,
            position_company_name: Optional[str] = None,
            can_user_process: bool = False
    ) -> TaskDto:
        """Convert CandidateApplication entity to TaskDto with enriched data

        Args:
            application: The application entity
            candidate_name: Candidate's full name (required)
            position_title: Job position title (required)
            current_stage_name: Name of current workflow stage (optional)
            candidate_email: Candidate's email (optional)
            candidate_photo_url: Candidate's photo URL (optional)
            position_company_name: Company name (optional)
            can_user_process: Whether user can process this task (optional)

        Returns:
            TaskDto with all enriched information
        """
        # Calculate priority
        priority = application.calculate_priority()

        # Calculate days in stage
        days_in_stage = 0
        if application.stage_entered_at:
            from datetime import datetime
            time_in_stage = datetime.utcnow() - application.stage_entered_at
            days_in_stage = time_in_stage.days

        # Check if overdue
        is_overdue = application.is_stage_deadline_passed()

        return TaskDto(
            # Application core fields
            application_id=application.id.value,
            candidate_id=application.candidate_id.value,
            job_position_id=application.job_position_id.value,
            application_status=application.application_status,
            applied_at=application.applied_at,
            updated_at=application.updated_at,

            # Workflow stage tracking
            current_stage_id=application.current_stage_id,
            current_stage_name=current_stage_name,
            stage_entered_at=application.stage_entered_at,
            stage_deadline=application.stage_deadline,
            task_status=application.task_status,

            # Enriched candidate information
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            candidate_photo_url=candidate_photo_url,

            # Enriched position information
            position_title=position_title,
            position_company_name=position_company_name,

            # Priority and metadata
            priority_score=priority.total_score,
            priority_level=priority.priority_level,
            days_in_stage=days_in_stage,
            is_overdue=is_overdue,

            # Assignment information
            can_user_process=can_user_process
        )
