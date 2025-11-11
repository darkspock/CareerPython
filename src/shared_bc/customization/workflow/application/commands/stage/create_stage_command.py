"""Create Stage Command."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from decimal import Decimal

from src.shared_bc.customization.workflow.domain.entities.workflow_stage import WorkflowStage
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.enums.kanban_display_enum import KanbanDisplayEnum
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_style import WorkflowStageStyle
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateStageCommand(Command):
    """Command to create a new workflow stage."""

    id: WorkflowStageId
    workflow_id: WorkflowId
    name: str
    description: str
    stage_type: WorkflowStageTypeEnum
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
    next_phase_id: Optional[PhaseId] = None  # Phase 12: Phase transition
    kanban_display: KanbanDisplayEnum = KanbanDisplayEnum.COLUMN  # Kanban display configuration
    style: Optional[WorkflowStageStyle] = None  # Visual styling
    validation_rules: Optional[Dict[str, Any]] = None  # JsonLogic validation rules
    recommended_rules: Optional[Dict[str, Any]] = None  # JsonLogic recommendation rules


class CreateStageCommandHandler(CommandHandler[CreateStageCommand]):
    """Handler for creating a new workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateStageCommand) -> None:
        """
        Handle the create stage command.

        Args:
            command: The create stage command
            
        Raises:
            ValueError: If trying to create a stage with INITIAL or SUCCESS type
                       when another stage with that type already exists in the workflow
        """
        # Validate that only one INITIAL and one SUCCESS stage can exist per workflow
        existing_stages = self.repository.list_by_workflow(command.workflow_id)
        
        if command.stage_type == WorkflowStageTypeEnum.INITIAL:
            initial_stages = [s for s in existing_stages if s.stage_type == WorkflowStageTypeEnum.INITIAL]
            if initial_stages:
                raise ValueError(
                    f"Workflow already has an INITIAL stage ({initial_stages[0].name}). "
                    "Only one INITIAL stage is allowed per workflow."
                )
        
        if command.stage_type == WorkflowStageTypeEnum.SUCCESS:
            success_stages = [s for s in existing_stages if s.stage_type == WorkflowStageTypeEnum.SUCCESS]
            if success_stages:
                raise ValueError(
                    f"Workflow already has a SUCCESS stage ({success_stages[0].name}). "
                    "Only one SUCCESS stage is allowed per workflow."
                )
        
        stage = WorkflowStage.create(
            id=command.id,
            workflow_id=command.workflow_id,
            name=command.name,
            description=command.description,
            stage_type=command.stage_type,
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
            next_phase_id=command.next_phase_id,
            kanban_display=command.kanban_display,
            style=command.style,
            validation_rules=command.validation_rules,
            recommended_rules=command.recommended_rules
        )

        self.repository.save(stage)
