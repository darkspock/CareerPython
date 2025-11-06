from dataclasses import dataclass
from datetime import datetime
from typing import Optional
# TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING

from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.workflow.domain.exceptions.invalid_workflow_operation import InvalidWorkFlowOperation
from src.workflow.domain.value_objects.workflow_id import WorkflowId

if TYPE_CHECKING:
    from src.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class Workflow:
    id: WorkflowId
    company_id: CompanyId
    workflow_type: WorkflowTypeEnum
    display: WorkflowDisplayEnum
    phase_id: Optional[PhaseId]  # Phase 12: Phase that this workflow belongs to
    name: str
    description: str
    status: WorkflowStatusEnum
    is_default: bool  # Is this the default workflow for the company?
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: WorkflowId,
            workflow_type: WorkflowTypeEnum,
            company_id: CompanyId,
            name: str,
            description: str,
            display: WorkflowDisplayEnum = WorkflowDisplayEnum.KANBAN,
            phase_id: Optional["PhaseId"] = None,
            is_default: bool = False
    ) -> "Workflow":
        """Factory method to create a new workflow"""
        if not name:
            raise ValueError("Workflow name cannot be empty")

        now = datetime.utcnow()
        return cls(
            id=id,
            company_id=company_id,
            workflow_type=workflow_type,
            display=display,
            phase_id=phase_id,
            name=name,
            description=description,
            status=WorkflowStatusEnum.DRAFT,  # Workflows start as DRAFT
            is_default=is_default,
            created_at=now,
            updated_at=now
        )

    def update(
            self,
            name: str,
            description: str,
            phase_id: Optional["PhaseId"] = None
    ) -> None:
        self.name = name
        self.description = description
        if phase_id is not None:
            self.phase_id = phase_id
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the workflow"""
        if self.status == WorkflowStatusEnum.ACTIVE:
            raise InvalidWorkFlowOperation("Workflow is already active")
        self.status = WorkflowStatusEnum.ACTIVE
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the workflow (move to draft)"""
        if self.status == WorkflowStatusEnum.DRAFT:
            raise InvalidWorkFlowOperation("Workflow is already in draft")

        if self.is_default:
            raise InvalidWorkFlowOperation("Cannot deactivate the default workflow")
        self.status = WorkflowStatusEnum.DRAFT
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive the workflow"""
        if self.status == WorkflowStatusEnum.ARCHIVED:
            raise InvalidWorkFlowOperation("Workflow is already archived")

        if self.is_default:
            raise InvalidWorkFlowOperation("Cannot archive the default workflow")
        self.status = WorkflowStatusEnum.ARCHIVED
        self.updated_at = datetime.utcnow()

    def set_as_default(self) -> None:
        """Set this workflow as the default for the company"""
        if self.status != WorkflowStatusEnum.ACTIVE:
            raise InvalidWorkFlowOperation("Only active workflows can be set as default")
        self.is_default = True
        self.updated_at = datetime.utcnow()

    def unset_as_default(self) -> None:
        """Remove this workflow as the default"""
        if not self.is_default:
            raise InvalidWorkFlowOperation("This workflow is not the default")
        self.is_default = False
        self.updated_at = datetime.utcnow()
