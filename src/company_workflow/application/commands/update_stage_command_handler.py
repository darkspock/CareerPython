"""Update Stage Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.update_stage_command import UpdateStageCommand
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.enums.stage_outcome import StageOutcome
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


class UpdateStageCommandHandler(CommandHandler[UpdateStageCommand, None]):
    """Handler for updating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, command: UpdateStageCommand) -> None:
        """
        Handle the update stage command.

        Args:
            command: The update stage command

        Raises:
            StageNotFound: If stage doesn't exist
        """
        stage_id = WorkflowStageId.from_string(command.id)
        stage = self.repository.get_by_id(stage_id)

        if not stage:
            raise StageNotFound(f"Stage with id {command.id} not found")

        required_outcome = None
        if command.required_outcome:
            required_outcome = StageOutcome(command.required_outcome)

        updated_stage = stage.update(
            name=command.name,
            description=command.description,
            required_outcome=required_outcome,
            estimated_duration_days=command.estimated_duration_days
        )

        self.repository.save(updated_stage)
