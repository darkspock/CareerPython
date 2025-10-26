"""
Task DTO
Phase 6: Data Transfer Object for task representation with enriched information
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.enums.task_status import TaskStatus


@dataclass
class TaskDto:
    """DTO for task representation with enriched candidate and position information"""

    # Application core fields
    application_id: str
    candidate_id: str
    job_position_id: str
    application_status: ApplicationStatusEnum
    applied_at: datetime
    updated_at: Optional[datetime]

    # Workflow stage tracking
    current_stage_id: Optional[str]
    current_stage_name: Optional[str]  # Enriched from workflow
    stage_entered_at: Optional[datetime]
    stage_deadline: Optional[datetime]
    task_status: TaskStatus

    # Enriched candidate information
    candidate_name: str
    candidate_email: Optional[str]
    candidate_photo_url: Optional[str]

    # Enriched position information
    position_title: str
    position_company_name: Optional[str]

    # Priority and metadata
    priority_score: int
    priority_level: str  # critical, high, medium, low
    days_in_stage: int
    is_overdue: bool

    # Assignment information
    can_user_process: bool  # Whether current user can process this task
