"""Interview Interviewer domain entity - represents the relationship between interviews and interviewers"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId


@dataclass
class InterviewInterviewer:
    """Represents an interviewer assigned to an interview
    
    This entity links a user (with GUEST role for external interviewers) to an interview.
    It allows tracking which users are interviewers for specific interviews.
    """
    id: InterviewInterviewerId
    interview_id: InterviewId
    user_id: UserId  # User ID of the interviewer (should have GUEST role for external interviewers)
    name: Optional[str] = None  # Display name (can be different from user name)
    is_external: bool = False  # True if interviewer is external (GUEST role)
    invited_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    def accept_invitation(self, accepted_by: Optional[str] = None) -> None:
        """Mark invitation as accepted"""
        if self.accepted_at:
            raise ValueError("Invitation already accepted")
        self.accepted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if accepted_by:
            self.updated_by = accepted_by

    def is_accepted(self) -> bool:
        """Check if invitation has been accepted"""
        return self.accepted_at is not None

    @staticmethod
    def create(
        id: InterviewInterviewerId,
        interview_id: InterviewId,
        user_id: UserId,
        name: Optional[str] = None,
        is_external: bool = False,
        created_by: Optional[str] = None
    ) -> 'InterviewInterviewer':
        """Create a new interview interviewer relationship"""
        now = datetime.utcnow()
        return InterviewInterviewer(
            id=id,
            interview_id=interview_id,
            user_id=user_id,
            name=name,
            is_external=is_external,
            invited_at=now,
            created_at=now,
            updated_at=now,
            created_by=created_by
        )

