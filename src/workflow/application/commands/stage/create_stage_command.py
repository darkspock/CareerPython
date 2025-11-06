"""Create Stage Command."""
from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal

from src.workflow.domain.entities.workflow_stage import WorkflowStage
from src.workflow.domain.enums.stage_type import StageType
from src.workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
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
    allow_skip: bool = False
    estimated_duration_days: Optional[int] = None
    is_active: bool = True
    default_role_ids: Optional[List[str]] = None
    default_assigned_users: Optional[List[str]] = None
    email_template_id: Optional[str] = None
    custom_email_text: Optional[str] = None
    deadline_days: Optional[int] = None
    estimated_cost: Optional[Decimal] = None
    next_phase_id: Optional[str] = None  # Phase 12: Phase transition


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
        stage_id = WorkflowStageId(command.id)
        workflow_id = WorkflowId(command.workflow_id)
        stage_type = StageType(command.stage_type)

        stage = WorkflowStage.create(
            id=stage_id,
            workflow_id=workflow_id,
            name=command.name,
            description=command.description,
            stage_type=stage_type,
            order=command.order,
            allow_skip=command.allow_skip,
            estimated_duration_days=command.estimated_duration_days,
            is_active=command.is_active,
            default_role_ids=command.default_role_ids,
            default_assigned_users=command.default_assigned_users,
            email_template_id=command.email_template_id,
            custom_email_text=command.custom_email_text,
            deadline_days=command.deadline_days,
            estimated_cost=command.estimated_cost,
            next_phase_id=command.next_phase_id  # Phase 12: Phase transition
        )

        self.repository.save(stage)
