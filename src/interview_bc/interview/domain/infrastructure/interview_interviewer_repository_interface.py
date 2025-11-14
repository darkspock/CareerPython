"""Interview Interviewer repository interface"""
from abc import ABC, abstractmethod
from typing import Optional, List

from src.interview_bc.interview.domain.entities.interview_interviewer import InterviewInterviewer
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId


class InterviewInterviewerRepositoryInterface(ABC):
    """Interface for Interview Interviewer repository"""

    @abstractmethod
    def create(self, interview_interviewer: InterviewInterviewer) -> InterviewInterviewer:
        """Create a new interview-interviewer relationship"""
        pass

    @abstractmethod
    def get_by_id(self, interviewer_id: str) -> Optional[InterviewInterviewer]:
        """Get interview interviewer by ID"""
        pass

    @abstractmethod
    def update(self, interview_interviewer: InterviewInterviewer) -> InterviewInterviewer:
        """Update an existing interview interviewer"""
        pass

    @abstractmethod
    def delete(self, interviewer_id: InterviewInterviewerId) -> bool:
        """Delete an interview interviewer relationship"""
        pass

    @abstractmethod
    def get_by_interview_id(self, interview_id: str) -> List[InterviewInterviewer]:
        """Get all interviewers for a specific interview"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[InterviewInterviewer]:
        """Get all interviews where a user is an interviewer"""
        pass

    @abstractmethod
    def get_by_interview_and_user(
            self,
            interview_id: str,
            user_id: str
    ) -> Optional[InterviewInterviewer]:
        """Get specific interviewer relationship by interview and user"""
        pass

    @abstractmethod
    def count_by_interview(self, interview_id: str) -> int:
        """Count interviewers for an interview"""
        pass

    @abstractmethod
    def is_user_interviewer(self, interview_id: str, user_id: str) -> bool:
        """Check if a user is an interviewer for an interview"""
        pass
