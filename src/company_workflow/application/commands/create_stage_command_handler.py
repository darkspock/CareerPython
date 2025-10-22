"""Create Stage Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.create_stage_command import CreateStageCommand
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.entities.workflow_stage import WorkflowStage
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.enums.stage_outcome import StageOutcome


class CreateStageCommandHandler(CommandHandler[CreateStageCommand, None]):
    """Handler for creating a new workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, command: CreateStageCommand) -> None:
        """
        Handle the create stage command.

        Args:
            command: The create stage command
        """
        stage_id = WorkflowStageId.from_string(command.id)
        workflow_id = CompanyWorkflowId.from_string(command.workflow_id)
        stage_type = StageType(command.stage_type)

        required_outcome = None
        if command.required_outcome:
            required_outcome = StageOutcome(command.required_outcome)

        stage = WorkflowStage.create(
            id=stage_id,
            workflow_id=workflow_id,
            name=command.name,
            description=command.description,
            stage_type=stage_type,
            order=command.order,
            required_outcome=required_outcome,
            estimated_duration_days=command.estimated_duration_days,
            is_active=command.is_active
        )

        self.repository.save(stage)
