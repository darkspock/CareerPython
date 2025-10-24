"""Update Stage Command."""
from dataclasses import dataclass
from typing import Optional

from src.company_workflow.domain.enums.stage_outcome import StageOutcome
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateStageCommand(Command):
    """Command to update a workflow stage."""

    id: str
    name: str
    description: str
    stage_type: str
    required_outcome: Optional[str] = None
    estimated_duration_days: Optional[int] = None


class UpdateStageCommandHandler(CommandHandler[UpdateStageCommand]):
    """Handler for updating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateStageCommand) -> None:
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

        stage_type = StageType(command.stage_type)

        updated_stage = stage.update(
            name=command.name,
            description=command.description,
            stage_type=stage_type,
            required_outcome=required_outcome,
            estimated_duration_days=command.estimated_duration_days
        )

        self.repository.save(updated_stage)
