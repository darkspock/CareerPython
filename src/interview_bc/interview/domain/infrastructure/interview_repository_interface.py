"""Interview repository interface"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewProcessTypeEnum
)
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview.domain.read_models.interview_list_read_model import InterviewListReadModel


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
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled' or 'deadline'
            has_scheduled_at_and_interviewers: bool = False,  # Special filter for "SCHEDULED" status
            limit: int = 50,
            offset: int = 0
    ) -> List[Interview]:
        """Find interviews by multiple filters"""
        pass

    @abstractmethod
    def count_by_filters(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled' or 'deadline'
            has_scheduled_at_and_interviewers: bool = False  # Special filter for "SCHEDULED" status
    ) -> int:
        """Count interviews matching the filters (for pagination)"""
        pass

    @abstractmethod
    def count_by_status(self, status: InterviewStatusEnum) -> int:
        """Count interviews by status"""
        pass

    @abstractmethod
    def count_by_candidate(self, candidate_id: str) -> int:
        """Count interviews for a candidate"""
        pass

    @abstractmethod
    def get_pending_interviews_by_candidate_and_stage(
            self,
            candidate_id: str,
            workflow_stage_id: str
    ) -> List[Interview]:
        """Get pending interviews for a candidate in a specific workflow stage"""
        pass

    @abstractmethod
    def get_by_token(self, interview_id: str, token: str) -> Optional[Interview]:
        """Get interview by ID and token for secure link access"""
        pass

    @abstractmethod
    def find_by_filters_with_joins(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled' or 'deadline'
            has_scheduled_at_and_interviewers: bool = False,  # Special filter for "SCHEDULED" status
            limit: int = 50,
            offset: int = 0
    ) -> List[InterviewListReadModel]:
        """Find interviews by multiple filters with JOINs to get all related information (ReadModel)"""
        pass

    @abstractmethod
    def count_by_filters(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled' or 'deadline'
            has_scheduled_at_and_interviewers: bool = False  # Special filter for "SCHEDULED" status
    ) -> int:
        """Count interviews matching the filters (for pagination)"""
        pass
