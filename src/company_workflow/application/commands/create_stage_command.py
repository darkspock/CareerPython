"""Create Stage Command."""
from dataclasses import dataclass
from typing import Optional

from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateStageCommand(Command):
    """Command to create a new workflow stage."""

    id: str
    workflow_id: str
    name: str
    description: str
    stage_type: str
    order: int
    required_outcome: Optional[str] = None
    estimated_duration_days: Optional[int] = None
    is_active: bool = True


class CreateStageCommandHandler(CommandHandler[CreateStageCommand]):
    """Handler for creating a new workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateStageCommand) -> None:
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
