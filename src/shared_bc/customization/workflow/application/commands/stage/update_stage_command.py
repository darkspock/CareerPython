"""Update Stage Command."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from decimal import Decimal

from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.enums.kanban_display_enum import KanbanDisplayEnum
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_style import WorkflowStageStyle
from src.shared_bc.customization.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateStageCommand(Command):
    """Command to update a workflow stage."""

    id: WorkflowStageId
    name: str
    description: str
    stage_type: WorkflowStageTypeEnum
    allow_skip: bool = False
    estimated_duration_days: Optional[int] = None
    default_role_ids: Optional[List[str]] = None
    default_assigned_users: Optional[List[str]] = None
    email_template_id: Optional[str] = None
    custom_email_text: Optional[str] = None
    deadline_days: Optional[int] = None
    estimated_cost: Optional[Decimal] = None
    next_phase_id: Optional[PhaseId] = None  # Phase 12: Phase transition
    style: Optional[WorkflowStageStyle] = None  # Stage style
    kanban_display: Optional[KanbanDisplayEnum] = None  # Kanban display configuration
    validation_rules: Optional[Dict[str, Any]] = None  # JsonLogic validation rules
    recommended_rules: Optional[Dict[str, Any]] = None  # JsonLogic recommendation rules


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
            WorkflowStageNotFound: If stage doesn't exist
        """
        stage = self.repository.get_by_id(command.id)

        if not stage:
            raise WorkflowStageNotFound(f"Stage with id {command.id} not found")

        # Update modifies the instance directly (mutability)
        stage.update(
            name=command.name,
            description=command.description,
            stage_type=command.stage_type,
            allow_skip=command.allow_skip,
            estimated_duration_days=command.estimated_duration_days,
            default_role_ids=command.default_role_ids,
            default_assigned_users=command.default_assigned_users,
            email_template_id=command.email_template_id,
            custom_email_text=command.custom_email_text,
            deadline_days=command.deadline_days,
            estimated_cost=command.estimated_cost,
            next_phase_id=command.next_phase_id,
            style=command.style,
            kanban_display=command.kanban_display,
            validation_rules=command.validation_rules,
            recommended_rules=command.recommended_rules
        )

        self.repository.save(stage)
