"""Interview Interviewer DTO"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.interview_bc.interview.domain.entities.interview_interviewer import InterviewInterviewer
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId


@dataclass
class InterviewInterviewerDto:
    id: InterviewInterviewerId
    interview_id: InterviewId
    user_id: UserId
    name: Optional[str]
    is_external: bool
    invited_at: Optional[datetime]
    accepted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: InterviewInterviewer) -> "InterviewInterviewerDto":
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id,
            interview_id=entity.interview_id,
            user_id=entity.user_id,
            name=entity.name,
            is_external=entity.is_external,
            invited_at=entity.invited_at,
            accepted_at=entity.accepted_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
