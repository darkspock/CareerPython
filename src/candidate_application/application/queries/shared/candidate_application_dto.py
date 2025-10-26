from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.enums.task_status import TaskStatus


@dataclass
class CandidateApplicationDto:
    """DTO para aplicaciones de candidatos"""
    id: str
    candidate_id: str
    job_position_id: str
    application_status: ApplicationStatusEnum
    applied_at: datetime
    updated_at: Optional[datetime]
    notes: Optional[str]
    # Phase 5: Workflow stage tracking fields
    current_stage_id: Optional[str] = None
    stage_entered_at: Optional[datetime] = None
    stage_deadline: Optional[datetime] = None
    task_status: TaskStatus = TaskStatus.PENDING
