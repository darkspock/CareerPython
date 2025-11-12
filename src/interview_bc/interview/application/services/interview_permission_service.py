"""Service for checking user permissions related to interviews"""
from typing import Optional

from src.company_bc.company.domain.enums import CompanyUserRole, CompanyUserStatus
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company_bc.company.domain.value_objects.company_id import CompanyId
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import \
    JobPositionRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.entities.interview_interviewer import InterviewInterviewer
from src.interview_bc.interview.domain.infrastructure.interview_interviewer_repository_interface import \
    InterviewInterviewerRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId


class InterviewPermissionService:
    """Service for validating user permissions related to interviews"""

    def __init__(
        self,
        company_user_repository: CompanyUserRepositoryInterface,
        interviewer_repository: InterviewInterviewerRepositoryInterface,
        company_candidate_repository: CompanyCandidateRepositoryInterface,
        job_position_repository: JobPositionRepositoryInterface
    ):
        self.company_user_repository = company_user_repository
        self.interviewer_repository = interviewer_repository
        self.company_candidate_repository = company_candidate_repository
        self.job_position_repository = job_position_repository

    def can_user_invite_interviewer(
        self,
        user_id: str,
        company_id: str,
        interview: Interview
    ) -> bool:
        """Check if a user can invite interviewers to an interview

        Args:
            user_id: ID of the user attempting to invite
            company_id: ID of the company (from token/auth)
            interview: The interview entity

        Returns:
            True if user can invite interviewers, False otherwise
        """
        # User must be part of the company
        company_user = self.company_user_repository.get_by_company_and_user(
            CompanyId.from_string(company_id),
            UserId.from_string(user_id)
        )

        if not company_user:
            return False

        # User must be active
        if company_user.status != CompanyUserStatus.ACTIVE:
            return False

        # Admins and recruiters can invite interviewers
        # GUEST role cannot invite others
        if company_user.role in [CompanyUserRole.ADMIN, CompanyUserRole.RECRUITER]:
            return True

        # Viewers cannot invite interviewers
        return False

    def can_user_accept_invitation(
        self,
        user_id: str,
        interviewer: InterviewInterviewer
    ) -> bool:
        """Check if a user can accept an interviewer invitation

        Args:
            user_id: ID of the user attempting to accept
            interviewer: The interviewer relationship entity

        Returns:
            True if user can accept, False otherwise
        """
        # User must be the one invited
        return str(interviewer.user_id) == user_id

    def can_user_access_interview(
        self,
        user_id: str,
        company_id: str,
        interview: Interview
    ) -> bool:
        """Check if a user can access an interview

        Args:
            user_id: ID of the user attempting to access
            company_id: ID of the company (from token/auth)
            interview: The interview entity

        Returns:
            True if user can access, False otherwise
        """
        # Check if user is part of the company
        company_user = self.company_user_repository.get_by_company_and_user(
            CompanyId.from_string(company_id),
            UserId.from_string(user_id)
        )

        if company_user and company_user.status == CompanyUserStatus.ACTIVE:
            # Company users can access interviews
            return True

        # Check if user is an interviewer for this interview
        interviewer = self.interviewer_repository.get_by_interview_and_user(
            str(interview.id),
            user_id
        )

        if interviewer and interviewer.is_accepted():
            # Accepted interviewers can access
            return True

        return False

    def can_user_modify_interview(
        self,
        user_id: str,
        company_id: str,
        interview: Interview
    ) -> bool:
        """Check if a user can modify an interview

        Args:
            user_id: ID of the user attempting to modify
            company_id: ID of the company (from token/auth)
            interview: The interview entity

        Returns:
            True if user can modify, False otherwise
        """
        # Only company users can modify interviews
        company_user = self.company_user_repository.get_by_company_and_user(
            CompanyId.from_string(company_id),
            UserId.from_string(user_id)
        )

        if not company_user:
            return False

        # User must be active
        if company_user.status != CompanyUserStatus.ACTIVE:
            return False

        # Admins and recruiters can modify interviews
        # Viewers and guests cannot modify
        return company_user.role in [CompanyUserRole.ADMIN, CompanyUserRole.RECRUITER]

    def is_user_interviewer_for_interview(
        self,
        user_id: str,
        interview_id: str
    ) -> bool:
        """Check if a user is an interviewer for an interview

        Args:
            user_id: ID of the user
            interview_id: ID of the interview

        Returns:
            True if user is an interviewer, False otherwise
        """
        interviewer = self.interviewer_repository.get_by_interview_and_user(
            interview_id,
            user_id
        )

        return interviewer is not None and interviewer.is_accepted()

    def does_interview_belong_to_company(
        self,
        interview: Interview,
        company_id: str
    ) -> bool:
        """Check if an interview belongs to a specific company

        Args:
            interview: The interview entity
            company_id: ID of the company to check

        Returns:
            True if interview belongs to company, False otherwise
        """
        company_id_vo = CompanyId.from_string(company_id)

        # Check via job_position if available
        if interview.job_position_id:
            job_position = self.job_position_repository.get_by_id(interview.job_position_id)
            if job_position and str(job_position.company_id) == company_id:
                return True

        # Check via candidate (through company_candidate relationship)
        if interview.candidate_id:
            # Get company candidates for this candidate
            company_candidates = self.company_candidate_repository.list_by_candidate(
                interview.candidate_id
            )
            # Check if any belongs to the company
            for cc in company_candidates:
                if str(cc.company_id) == company_id:
                    return True

        return False

    def can_user_access_interview_by_company(
        self,
        user_id: str,
        company_id: str,
        interview: Interview
    ) -> bool:
        """Check if a user can access an interview, verifying it belongs to the company

        Args:
            user_id: ID of the user attempting to access
            company_id: ID of the company (from token/auth)
            interview: The interview entity

        Returns:
            True if user can access, False otherwise
        """
        # First verify interview belongs to company
        if not self.does_interview_belong_to_company(interview, company_id):
            return False

        # Then check user permissions
        return self.can_user_access_interview(user_id, company_id, interview)

    def can_user_modify_interview_by_company(
        self,
        user_id: str,
        company_id: str,
        interview: Interview
    ) -> bool:
        """Check if a user can modify an interview, verifying it belongs to the company

        Args:
            user_id: ID of the user attempting to modify
            company_id: ID of the company (from token/auth)
            interview: The interview entity

        Returns:
            True if user can modify, False otherwise
        """
        # First verify interview belongs to company
        if not self.does_interview_belong_to_company(interview, company_id):
            return False

        # Then check user permissions
        return self.can_user_modify_interview(user_id, company_id, interview)

