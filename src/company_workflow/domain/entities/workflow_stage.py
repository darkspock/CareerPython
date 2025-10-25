from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.enums.stage_type import StageType


@dataclass(frozen=True)
class WorkflowStage:
    """Workflow stage entity - represents a stage in a recruitment workflow"""
    id: WorkflowStageId
    workflow_id: CompanyWorkflowId
    name: str
    description: str
    stage_type: StageType
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

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: WorkflowStageId,
        workflow_id: CompanyWorkflowId,
        name: str,
        description: str,
        stage_type: StageType,
        order: int,
        allow_skip: bool = False,
        estimated_duration_days: Optional[int] = None,
        is_active: bool = True,
        default_role_ids: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[str] = None,
        custom_email_text: Optional[str] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None
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

        now = datetime.utcnow()
        return WorkflowStage(
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
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        name: str,
        description: str,
        stage_type: StageType,
        allow_skip: bool,
        estimated_duration_days: Optional[int],
        default_role_ids: Optional[List[str]] = None,
        default_assigned_users: Optional[List[str]] = None,
        email_template_id: Optional[str] = None,
        custom_email_text: Optional[str] = None,
        deadline_days: Optional[int] = None,
        estimated_cost: Optional[Decimal] = None
    ) -> "WorkflowStage":
        """Update stage information"""
        if not name:
            raise ValueError("Stage name cannot be empty")
        if estimated_duration_days is not None and estimated_duration_days < 0:
            raise ValueError("Estimated duration must be non-negative")
        if deadline_days is not None and deadline_days < 1:
            raise ValueError("Deadline must be at least 1 day")
        if estimated_cost is not None and estimated_cost < 0:
            raise ValueError("Estimated cost must be non-negative")

        return WorkflowStage(
            id=self.id,
            workflow_id=self.workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=self.order,
            allow_skip=allow_skip,
            estimated_duration_days=estimated_duration_days,
            is_active=self.is_active,
            default_role_ids=default_role_ids if default_role_ids is not None else self.default_role_ids,
            default_assigned_users=default_assigned_users if default_assigned_users is not None else self.default_assigned_users,
            email_template_id=email_template_id if email_template_id is not None else self.email_template_id,
            custom_email_text=custom_email_text if custom_email_text is not None else self.custom_email_text,
            deadline_days=deadline_days if deadline_days is not None else self.deadline_days,
            estimated_cost=estimated_cost if estimated_cost is not None else self.estimated_cost,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def reorder(self, new_order: int) -> "WorkflowStage":
        """Change the order of this stage"""
        if new_order < 0:
            raise ValueError("Stage order must be non-negative")

        return WorkflowStage(
            id=self.id,
            workflow_id=self.workflow_id,
            name=self.name,
            description=self.description,
            stage_type=self.stage_type,
            order=new_order,
            allow_skip=self.allow_skip,
            estimated_duration_days=self.estimated_duration_days,
            is_active=self.is_active,
            default_role_ids=self.default_role_ids,
            default_assigned_users=self.default_assigned_users,
            email_template_id=self.email_template_id,
            custom_email_text=self.custom_email_text,
            deadline_days=self.deadline_days,
            estimated_cost=self.estimated_cost,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def activate(self) -> "WorkflowStage":
        """Activate this stage"""
        return WorkflowStage(
            id=self.id,
            workflow_id=self.workflow_id,
            name=self.name,
            description=self.description,
            stage_type=self.stage_type,
            order=self.order,
            allow_skip=self.allow_skip,
            estimated_duration_days=self.estimated_duration_days,
            is_active=True,
            default_role_ids=self.default_role_ids,
            default_assigned_users=self.default_assigned_users,
            email_template_id=self.email_template_id,
            custom_email_text=self.custom_email_text,
            deadline_days=self.deadline_days,
            estimated_cost=self.estimated_cost,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def deactivate(self) -> "WorkflowStage":
        """Deactivate this stage"""
        return WorkflowStage(
            id=self.id,
            workflow_id=self.workflow_id,
            name=self.name,
            description=self.description,
            stage_type=self.stage_type,
            order=self.order,
            allow_skip=self.allow_skip,
            estimated_duration_days=self.estimated_duration_days,
            is_active=False,
            default_role_ids=self.default_role_ids,
            default_assigned_users=self.default_assigned_users,
            email_template_id=self.email_template_id,
            custom_email_text=self.custom_email_text,
            deadline_days=self.deadline_days,
            estimated_cost=self.estimated_cost,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
