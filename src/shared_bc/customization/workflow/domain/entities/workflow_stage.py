from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
# TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING

from src.shared_bc.customization.workflow.domain.enums.kanban_display_enum import KanbanDisplayEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import \
    WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_style import WorkflowStageStyle

if TYPE_CHECKING:
    from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
    from src.interview_bc.interview.domain.value_objects.interview_configuration import InterviewConfiguration
else:
    from src.interview_bc.interview.domain.value_objects.interview_configuration import InterviewConfiguration


@dataclass
class WorkflowStage:
    """Workflow stage entity - represents a stage in a recruitment workflow"""
    id: WorkflowStageId
    workflow_id: WorkflowId
    name: str
    description: str
    stage_type: WorkflowStageTypeEnum
    order: int  # Position in the workflow
    allow_skip: bool  # Whether this stage can be skipped (optional stage)
    estimated_duration_days: Optional[int]  # Estimated days in this stage
    is_active: bool

    # Phase 2: Enhanced configuration fields
    default_role_ids: Optional[List[str]]  # Role IDs that should be assigned to this stage
    default_assigned_users: Optional[List[str]]  # User IDs always assigned to this stage
    email_template_id: Optional[str]  # Email template to use when entering stage
    custom_email_text: Optional[str]  # Additional text for email template
    deadline_days: Optional[int]  # Days to complete this stage (for task priority)
    estimated_cost: Optional[Decimal]  # Estimated cost for this stage

    # Phase 12: Phase transition
    next_phase_id: Optional["PhaseId"]  # Phase to transition to when reaching this stage (only for SUCCESS/FAIL stages)

    # Kanban display configuration
    kanban_display: KanbanDisplayEnum  # 'column', 'row', or 'none'

    # Visual styling
    style: WorkflowStageStyle

    # JsonLogic validation and recommendation rules
    validation_rules: Optional[dict]  # JsonLogic rules that must pass to proceed
    recommended_rules: Optional[dict]  # JsonLogic rules that are recommended but not required

    # Interview configuration
    interview_configurations: Optional[
        List[InterviewConfiguration]]  # List of interview configurations (template_id + mode) for this stage

    # Field properties configuration per custom field
    # Structure: {field_id: {is_required: bool, is_read_only: bool, visible_hr: bool, visible_candidate: bool}}
    field_properties_config: Optional[Dict[str, Any]]

    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: WorkflowStageId,
            workflow_id: WorkflowId,
            name: str,
            description: str,
            stage_type: WorkflowStageTypeEnum,
            order: int,
            allow_skip: bool = False,
            estimated_duration_days: Optional[int] = None,
            is_active: bool = True,
            default_role_ids: Optional[List[str]] = None,
            default_assigned_users: Optional[List[str]] = None,
            email_template_id: Optional[str] = None,
            custom_email_text: Optional[str] = None,
            deadline_days: Optional[int] = None,
            estimated_cost: Optional[Decimal] = None,
            next_phase_id: Optional["PhaseId"] = None,
            kanban_display: KanbanDisplayEnum = KanbanDisplayEnum.COLUMN,
            style: Optional[WorkflowStageStyle] = None,
            validation_rules: Optional[dict] = None,
            recommended_rules: Optional[dict] = None,
            interview_configurations: Optional[List[InterviewConfiguration]] = None,
            field_properties_config: Optional[Dict[str, Any]] = None
    ) -> "WorkflowStage":
        """Factory method to create a new workflow stage"""
        if not name:
            raise ValueError("Stage name cannot be empty")
        if order < 0:
            raise ValueError("Stage order must be non-negative")
        if estimated_duration_days is not None and estimated_duration_days < 0:
            raise ValueError("Estimated duration must be non-negative")
        if deadline_days is not None and deadline_days < 1:
            raise ValueError("Deadline must be at least 1 day")
        if estimated_cost is not None and estimated_cost < 0:
            raise ValueError("Estimated cost must be non-negative")

        # Validate next_phase_id can only be set for SUCCESS or FAIL stages
        if next_phase_id is not None and stage_type not in [WorkflowStageTypeEnum.SUCCESS, WorkflowStageTypeEnum.FAIL]:
            raise ValueError("next_phase_id can only be set for SUCCESS or FAIL stage types")

        # Determine default style based on stage type if not provided
        if style is None:
            # Default style for all stage types
            style = WorkflowStageStyle(
                background_color="#ffffff",
                text_color="#000000",
                icon=""
            )

        now = datetime.utcnow()
        return cls(
            id=id,
            workflow_id=workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=order,
            allow_skip=allow_skip,
            estimated_duration_days=estimated_duration_days,
            is_active=is_active,
            default_role_ids=default_role_ids or [],
            default_assigned_users=default_assigned_users or [],
            email_template_id=email_template_id,
            custom_email_text=custom_email_text,
            deadline_days=deadline_days,
            estimated_cost=estimated_cost,
            next_phase_id=next_phase_id,
            kanban_display=kanban_display,
            style=style,
            validation_rules=validation_rules,
            recommended_rules=recommended_rules,
            interview_configurations=interview_configurations or [],
            field_properties_config=field_properties_config,
            created_at=now,
            updated_at=now
        )

    def update(
            self,
            name: str,
            description: str,
            stage_type: WorkflowStageTypeEnum,
            allow_skip: bool,
            estimated_duration_days: Optional[int],
            default_role_ids: Optional[List[str]] = None,
            default_assigned_users: Optional[List[str]] = None,
            email_template_id: Optional[str] = None,
            custom_email_text: Optional[str] = None,
            deadline_days: Optional[int] = None,
            estimated_cost: Optional[Decimal] = None,
            next_phase_id: Optional["PhaseId"] = None,
            style: Optional[WorkflowStageStyle] = None,
            kanban_display: Optional[KanbanDisplayEnum] = None,
            validation_rules: Optional[dict] = None,
            recommended_rules: Optional[dict] = None,
            interview_configurations: Optional[List[InterviewConfiguration]] = None,
            field_properties_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update stage information"""
        if not name:
            raise ValueError("Stage name cannot be empty")
        if estimated_duration_days is not None and estimated_duration_days < 0:
            raise ValueError("Estimated duration must be non-negative")
        if deadline_days is not None and deadline_days < 1:
            raise ValueError("Deadline must be at least 1 day")
        if estimated_cost is not None and estimated_cost < 0:
            raise ValueError("Estimated cost must be non-negative")

        # Validate next_phase_id can only be set for SUCCESS or FAIL stages
        if next_phase_id is not None and stage_type not in [WorkflowStageTypeEnum.SUCCESS, WorkflowStageTypeEnum.FAIL]:
            raise ValueError("next_phase_id can only be set for SUCCESS or FAIL stage types")

        # Modify the instance directly (mutability)
        self.name = name
        self.description = description
        self.stage_type = stage_type
        self.allow_skip = allow_skip
        self.estimated_duration_days = estimated_duration_days
        self.default_role_ids = default_role_ids if default_role_ids is not None else self.default_role_ids
        self.default_assigned_users = default_assigned_users if default_assigned_users is not None else self.default_assigned_users
        self.email_template_id = email_template_id if email_template_id is not None else self.email_template_id
        self.custom_email_text = custom_email_text if custom_email_text is not None else self.custom_email_text
        self.deadline_days = deadline_days if deadline_days is not None else self.deadline_days
        self.estimated_cost = estimated_cost if estimated_cost is not None else self.estimated_cost
        self.next_phase_id = next_phase_id if next_phase_id is not None else self.next_phase_id
        self.kanban_display = kanban_display if kanban_display is not None else self.kanban_display
        self.style = style if style is not None else self.style
        self.validation_rules = validation_rules if validation_rules is not None else self.validation_rules
        self.recommended_rules = recommended_rules if recommended_rules is not None else self.recommended_rules
        self.interview_configurations = interview_configurations if interview_configurations is not None else self.interview_configurations
        self.field_properties_config = field_properties_config if field_properties_config is not None else self.field_properties_config
        self.updated_at = datetime.utcnow()

    def reorder(self, new_order: int) -> None:
        """Change the order of this stage"""
        if new_order < 0:
            raise ValueError("Stage order must be non-negative")

        self.order = new_order
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate this stage"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate this stage"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
