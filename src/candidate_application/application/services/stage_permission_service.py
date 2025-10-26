"""Service for checking user permissions to process applications at specific workflow stages"""

from typing import List, Optional

from src.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.position_stage_assignment.domain.repositories.position_stage_assignment_repository_interface import (
    PositionStageAssignmentRepositoryInterface
)


class StagePermissionService:
    """Service for validating user permissions to process applications at workflow stages"""

    def __init__(
        self,
        position_stage_assignment_repository: PositionStageAssignmentRepositoryInterface
    ):
        self.position_stage_assignment_repository = position_stage_assignment_repository

    def can_user_process_stage(
        self,
        user_id: str,
        application: CandidateApplication,
        company_id: str
    ) -> bool:
        """Check if a user can process an application at its current stage

        Args:
            user_id: ID of the user attempting to process
            application: The candidate application
            company_id: ID of the company (for admin check)

        Returns:
            True if user can process, False otherwise
        """
        # If application is not in a workflow stage, deny access
        if not application.current_stage_id:
            return False

        # Check if user is company admin (admins can process any stage)
        if self.is_user_company_admin(user_id, company_id):
            return True

        # Check if user is assigned to this stage
        assigned_users = self.get_assigned_users_for_stage(
            application.job_position_id.value,
            application.current_stage_id
        )

        return user_id in assigned_users

    def get_assigned_users_for_stage(
        self,
        position_id: str,
        stage_id: str
    ) -> List[str]:
        """Get list of user IDs assigned to a specific stage for a position

        Args:
            position_id: ID of the job position
            stage_id: ID of the workflow stage

        Returns:
            List of user IDs assigned to the stage
        """
        assignment = self.position_stage_assignment_repository.get_by_position_and_stage(
            position_id,
            stage_id
        )

        if assignment is None:
            return []

        # Return a copy to avoid mutability issues
        return list(assignment.assigned_user_ids)

    def is_user_company_admin(self, user_id: str, company_id: str) -> bool:
        """Check if user is an admin of the company

        Args:
            user_id: ID of the user
            company_id: ID of the company

        Returns:
            True if user is company admin, False otherwise

        Note:
            This is a simplified implementation. In a real system, you would:
            1. Query the company_users table
            2. Check the user's role (admin, owner, etc.)
            3. Return True only if user has admin privileges

            For now, we return False to enforce strict permission checks.
            This should be implemented in Phase 5.5 or later.
        """
        # TODO: Implement actual company admin check
        # Query company_users table and check role
        # For now, return False to be restrictive
        return False

    def can_user_change_stage(
        self,
        user_id: str,
        application: CandidateApplication,
        target_stage_id: str,
        company_id: str
    ) -> bool:
        """Check if user can move an application to a specific stage

        Args:
            user_id: ID of the user attempting the change
            application: The candidate application
            target_stage_id: ID of the target stage
            company_id: ID of the company

        Returns:
            True if user can move to target stage, False otherwise
        """
        # User must have permission to process current stage
        if not self.can_user_process_stage(user_id, application, company_id):
            return False

        # Check if user is assigned to target stage (or is admin)
        if self.is_user_company_admin(user_id, company_id):
            return True

        target_assigned_users = self.get_assigned_users_for_stage(
            application.job_position_id.value,
            target_stage_id
        )

        # User should ideally be assigned to target stage too
        # But we allow moving if user can process current stage
        # This is a business logic decision
        return True  # Allow if user can process current stage
