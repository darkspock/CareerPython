from dataclasses import dataclass
from typing import Optional

from src.company_bc.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum


@dataclass(frozen=True)
class ChangeStageCommand(Command):
    """Command to change the workflow stage of a company candidate"""
    id: CompanyCandidateId
    new_stage_id: WorkflowStageId


class ChangeStageCommandHandler(CommandHandler[ChangeStageCommand]):
    """Handler for changing the workflow stage of a company candidate with automatic phase transition support"""

    def __init__(
        self,
        repository: CompanyCandidateRepositoryInterface,
        workflow_stage_repository: WorkflowStageRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface
    ):
        self._repository = repository
        self._workflow_stage_repository = workflow_stage_repository
        self._workflow_repository = workflow_repository

    def execute(self, command: ChangeStageCommand) -> None:
        """Handle the change stage command with automatic phase transition
        
        If the target stage is SUCCESS and has a next_phase_id configured,
        automatically transitions the candidate to the next phase.
        """
        # Get existing company candidate
        company_candidate_id = command.id
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Get the target workflow stage
        target_stage = self._workflow_stage_repository.get_by_id(command.new_stage_id)
        if not target_stage:
            raise ValueError(f"Stage {command.new_stage_id.value} not found")

        # Change stage
        updated_candidate = company_candidate.change_stage(new_stage_id=command.new_stage_id)

        # Check if this is a SUCCESS stage with next_phase_id configured
        if target_stage.stage_type == WorkflowStageTypeEnum.SUCCESS and target_stage.next_phase_id:
            # Get workflows for the next phase (filter by CANDIDATE_APPLICATION type)
            next_phase_workflows = self._workflow_repository.list_by_phase_id(
                target_stage.next_phase_id,
                workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION
            )
            
            if not next_phase_workflows:
                # No workflow found for next phase, just update the stage
                self._repository.save(updated_candidate)
                return

            # Use the first workflow (or default if available)
            next_phase_workflow = next((w for w in next_phase_workflows if w.is_default), None) or next_phase_workflows[0]

            # Get the initial stage of the next phase's workflow
            initial_stage = self._workflow_stage_repository.get_initial_stage(next_phase_workflow.id)
            if not initial_stage:
                # No initial stage found, just update the stage
                self._repository.save(updated_candidate)
                return

            # Automatically transition to the next phase
            # Use updated_candidate to preserve the stage change, then move to next phase
            updated_candidate = updated_candidate.move_to_next_phase(
                next_phase_id=target_stage.next_phase_id,
                next_workflow_id=next_phase_workflow.id,
                initial_stage_id=initial_stage.id
            )

        # Save to repository
        self._repository.save(updated_candidate)
