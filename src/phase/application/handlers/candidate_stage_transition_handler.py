"""Handler for candidate stage transitions that trigger phase changes

Phase 12: When a candidate reaches a SUCCESS or FAIL terminal stage,
this handler checks if the stage has a next_phase_id configured and
automatically moves the candidate to the next phase.
"""
from typing import Optional

from src.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import \
    CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.enums.stage_type import StageType


class CandidateStageTransitionHandler:
    """Handler for stage transitions that may trigger phase changes

    This handler is called whenever a candidate moves to a new stage.
    If the new stage is a terminal stage (SUCCESS or FAIL) with a next_phase_id,
    it automatically moves the candidate to the next phase.
    """

    def __init__(
        self,
        application_repository: CandidateApplicationRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface,
        workflow_repository: CompanyWorkflowRepositoryInterface
    ):
        self.application_repository = application_repository
        self.stage_repository = stage_repository
        self.workflow_repository = workflow_repository

    def handle_stage_transition(
        self,
        application_id: CandidateApplicationId,
        new_stage_id: str
    ) -> None:
        """Handle a stage transition and check if phase change is needed

        Args:
            application_id: ID of the candidate application
            new_stage_id: ID of the new stage the candidate moved to
        """
        # Get the application
        application = self.application_repository.get_by_id(application_id)
        if not application:
            return

        # Get the stage
        stage = self.stage_repository.get_by_id(WorkflowStageId.from_string(new_stage_id))
        if not stage:
            return

        # Check if this is a terminal stage with next_phase_id
        if stage.stage_type not in [StageType.SUCCESS, StageType.FAIL]:
            return

        if not stage.next_phase_id:
            return

        # This is a terminal stage with phase transition configured
        # Find the initial stage of the default workflow in the next phase
        next_phase_initial_stage = self._get_phase_initial_stage(stage.next_phase_id)

        if not next_phase_initial_stage:
            # No workflow found for next phase, just update phase_id
            application.move_to_next_phase(
                next_phase_id=stage.next_phase_id,
                initial_stage_id=None,
                time_limit_hours=None
            )
        else:
            # Move to next phase with initial stage
            time_limit_hours = None
            if next_phase_initial_stage.estimated_duration_days:
                time_limit_hours = next_phase_initial_stage.estimated_duration_days * 24

            application.move_to_next_phase(
                next_phase_id=stage.next_phase_id,
                initial_stage_id=next_phase_initial_stage.id.value,
                time_limit_hours=time_limit_hours
            )

        # Save the updated application
        self.application_repository.save(application)

    def _get_phase_initial_stage(self, phase_id: str) -> Optional[any]:
        """Get the initial stage of the default workflow for a phase

        Args:
            phase_id: ID of the phase

        Returns:
            The initial stage of the default workflow, or None if not found
        """
        # Find workflows for this phase
        # Note: We need a method to list workflows by phase_id
        # For now, this is a placeholder that needs to be implemented
        # when we add list_by_phase method to workflow repository

        # TODO: Implement this when we add list_by_phase_id to workflow repository
        # For now, return None
        return None
