"""Service for validating pending interviews in workflow stages"""
from typing import List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class InterviewValidationService:
    """Service for validating pending interviews in workflow stages"""

    def __init__(
            self,
            interview_repository: InterviewRepositoryInterface
    ):
        self.interview_repository = interview_repository

    def has_pending_interviews(
            self,
            candidate_id: CandidateId,
            workflow_stage_id: WorkflowStageId
    ) -> bool:
        """
        Check if a candidate has pending interviews in a specific workflow stage.

        Args:
            candidate_id: The candidate ID
            workflow_stage_id: The workflow stage ID

        Returns:
            True if there are pending interviews, False otherwise
        """
        pending_interviews = self.interview_repository.get_pending_interviews_by_candidate_and_stage(
            candidate_id=str(candidate_id),
            workflow_stage_id=str(workflow_stage_id)
        )
        return len(pending_interviews) > 0

    def get_pending_interviews_count(
            self,
            candidate_id: CandidateId,
            workflow_stage_id: WorkflowStageId
    ) -> int:
        """
        Get the count of pending interviews for a candidate in a specific workflow stage.

        Args:
            candidate_id: The candidate ID
            workflow_stage_id: The workflow stage ID

        Returns:
            Number of pending interviews
        """
        pending_interviews = self.interview_repository.get_pending_interviews_by_candidate_and_stage(
            candidate_id=str(candidate_id),
            workflow_stage_id=str(workflow_stage_id)
        )
        return len(pending_interviews)

    def get_pending_interviews(
            self,
            candidate_id: CandidateId,
            workflow_stage_id: WorkflowStageId
    ) -> List:
        """
        Get all pending interviews for a candidate in a specific workflow stage.

        Args:
            candidate_id: The candidate ID
            workflow_stage_id: The workflow stage ID

        Returns:
            List of pending interviews
        """
        return self.interview_repository.get_pending_interviews_by_candidate_and_stage(
            candidate_id=str(candidate_id),
            workflow_stage_id=str(workflow_stage_id)
        )
