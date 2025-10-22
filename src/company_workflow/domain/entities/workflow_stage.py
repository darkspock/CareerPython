from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.enums.stage_outcome import StageOutcome


@dataclass(frozen=True)
class WorkflowStage:
    """Workflow stage entity - represents a stage in a recruitment workflow"""
    id: WorkflowStageId
    workflow_id: CompanyWorkflowId
    name: str
    description: str
    stage_type: StageType
    order: int  # Position in the workflow
    required_outcome: Optional[StageOutcome]  # Required outcome to proceed
    estimated_duration_days: Optional[int]  # Estimated days in this stage
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: WorkflowStageId,
        workflow_id: CompanyWorkflowId,
        name: str,
        description: str,
        stage_type: StageType,
        order: int,
        required_outcome: Optional[StageOutcome] = None,
        estimated_duration_days: Optional[int] = None
    ) -> "WorkflowStage":
        """Factory method to create a new workflow stage"""
        if not name:
            raise ValueError("Stage name cannot be empty")
        if order < 0:
            raise ValueError("Stage order must be non-negative")
        if estimated_duration_days is not None and estimated_duration_days < 0:
            raise ValueError("Estimated duration must be non-negative")

        now = datetime.utcnow()
        return cls(
            id=id,
            workflow_id=workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=order,
            required_outcome=required_outcome,
            estimated_duration_days=estimated_duration_days,
            is_active=True,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        name: str,
        description: str,
        stage_type: StageType,
        required_outcome: Optional[StageOutcome],
        estimated_duration_days: Optional[int]
    ) -> "WorkflowStage":
        """Update stage information"""
        if not name:
            raise ValueError("Stage name cannot be empty")
        if estimated_duration_days is not None and estimated_duration_days < 0:
            raise ValueError("Estimated duration must be non-negative")

        return WorkflowStage(
            id=self.id,
            workflow_id=self.workflow_id,
            name=name,
            description=description,
            stage_type=stage_type,
            order=self.order,
            required_outcome=required_outcome,
            estimated_duration_days=estimated_duration_days,
            is_active=self.is_active,
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
            required_outcome=self.required_outcome,
            estimated_duration_days=self.estimated_duration_days,
            is_active=self.is_active,
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
            required_outcome=self.required_outcome,
            estimated_duration_days=self.estimated_duration_days,
            is_active=True,
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
            required_outcome=self.required_outcome,
            estimated_duration_days=self.estimated_duration_days,
            is_active=False,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
