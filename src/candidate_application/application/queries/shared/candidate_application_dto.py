from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum


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
