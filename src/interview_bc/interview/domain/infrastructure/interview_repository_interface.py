"""Interview repository interface"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from src.interview.interview.domain.entities.interview import Interview
from src.interview.interview.domain.enums.interview_enums import InterviewStatusEnum, InterviewTypeEnum
from src.interview.interview.domain.value_objects.interview_id import InterviewId


class InterviewRepositoryInterface(ABC):
    """Interface for Interview repository"""

    @abstractmethod
    def create(self, interview: Interview) -> Interview:
        """Create a new interview"""
        pass

    @abstractmethod
    def get_by_id(self, interview_id: str) -> Optional[Interview]:
        """Get interview by ID"""
        pass

    @abstractmethod
    def update(self, interview: Interview) -> Interview:
        """Update an existing interview"""
        pass

    @abstractmethod
    def delete(self, id: InterviewId) -> bool:
        """Delete an interview"""
        pass

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: str) -> List[Interview]:
        """Get all interviews for a candidate"""
        pass

    @abstractmethod
    def get_by_job_position_id(self, job_position_id: str) -> List[Interview]:
        """Get all interviews for a job position"""
        pass

    @abstractmethod
    def get_by_status(self, status: InterviewStatusEnum) -> List[Interview]:
        """Get interviews by status"""
        pass

    @abstractmethod
    def get_by_interview_type(self, interview_type: InterviewTypeEnum) -> List[Interview]:
        """Get interviews by type"""
        pass

    @abstractmethod
    def get_scheduled_interviews(self, from_date: datetime, to_date: datetime) -> List[Interview]:
        """Get scheduled interviews within date range"""
        pass

    @abstractmethod
    def get_interviews_by_candidate_and_job_position(
            self,
            candidate_id: str,
            job_position_id: str
    ) -> List[Interview]:
        """Get interviews for specific candidate and job position"""
        pass

    @abstractmethod
    def find_by_filters(
            self,
            candidate_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            limit: int = 50,
            offset: int = 0
    ) -> List[Interview]:
        """Find interviews by multiple filters"""
        pass

    @abstractmethod
    def count_by_status(self, status: InterviewStatusEnum) -> int:
        """Count interviews by status"""
        pass

    @abstractmethod
    def count_by_candidate(self, candidate_id: str) -> int:
        """Count interviews for a candidate"""
        pass
