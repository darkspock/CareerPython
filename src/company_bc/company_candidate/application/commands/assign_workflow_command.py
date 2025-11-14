from dataclasses import dataclass

from src.company_bc.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.services.stage_phase_validation_service import \
    StagePhaseValidationService
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class AssignWorkflowCommand(Command):
    """Command to assign a workflow to a company candidate"""
    id: CompanyCandidateId
    workflow_id: WorkflowId
    initial_stage_id: WorkflowStageId


class AssignWorkflowCommandHandler(CommandHandler[AssignWorkflowCommand]):
    """Handler for assigning a workflow to a company candidate"""

    def __init__(
            self,
            repository: CompanyCandidateRepositoryInterface,
            validation_service: StagePhaseValidationService
    ):
        self._repository = repository
        self._validation_service = validation_service

    def execute(self, command: AssignWorkflowCommand) -> None:
        """Handle the assign workflow command"""
        # Get existing company candidate
        company_candidate_id = command.id
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Validate stage belongs to workflow using Domain Service
        try:
            self._validation_service.validate_stage_belongs_to_workflow(
                stage_id=command.initial_stage_id,
                workflow_id=command.workflow_id
            )
        except ValueError as e:
            raise ValueError(f"Cannot assign workflow: {e}")

        # Validate workflow has phase_id using Domain Service
        try:
            workflow_phase_id = self._validation_service.validate_workflow_has_phase(command.workflow_id)
        except ValueError as e:
            raise ValueError(f"Cannot assign workflow: {e}")

        # Assign workflow (with phase_id from validation)
        updated_candidate = company_candidate.assign_workflow(
            workflow_id=command.workflow_id,
            initial_stage_id=command.initial_stage_id,
            phase_id=workflow_phase_id
        )

        # Save to repository
        self._repository.save(updated_candidate)
