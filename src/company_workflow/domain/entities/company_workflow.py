from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus
from src.company_workflow.domain.exceptions.invalid_workflow_operation import InvalidWorkflowOperation


@dataclass(frozen=True)
class CompanyWorkflow:
    """Company workflow entity - represents a custom recruitment workflow"""
    id: CompanyWorkflowId
    company_id: CompanyId
    name: str
    description: str
    status: WorkflowStatus
    is_default: bool  # Is this the default workflow for the company?
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: CompanyWorkflowId,
        company_id: CompanyId,
        name: str,
        description: str,
        is_default: bool = False
    ) -> "CompanyWorkflow":
        """Factory method to create a new company workflow"""
        if not name:
            raise ValueError("Workflow name cannot be empty")

        now = datetime.utcnow()
        return cls(
            id=id,
            company_id=company_id,
            name=name,
            description=description,
            status=WorkflowStatus.ACTIVE,
            is_default=is_default,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        name: str,
        description: str
    ) -> "CompanyWorkflow":
        """Update workflow information"""
        if not name:
            raise ValueError("Workflow name cannot be empty")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=name,
            description=description,
            status=self.status,
            is_default=self.is_default,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def activate(self) -> "CompanyWorkflow":
        """Activate the workflow"""
        if self.status == WorkflowStatus.ACTIVE:
            raise InvalidWorkflowOperation("Workflow is already active")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            status=WorkflowStatus.ACTIVE,
            is_default=self.is_default,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def deactivate(self) -> "CompanyWorkflow":
        """Deactivate the workflow"""
        if self.status == WorkflowStatus.INACTIVE:
            raise InvalidWorkflowOperation("Workflow is already inactive")

        if self.is_default:
            raise InvalidWorkflowOperation("Cannot deactivate the default workflow")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            status=WorkflowStatus.INACTIVE,
            is_default=self.is_default,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def archive(self) -> "CompanyWorkflow":
        """Archive the workflow"""
        if self.status == WorkflowStatus.ARCHIVED:
            raise InvalidWorkflowOperation("Workflow is already archived")

        if self.is_default:
            raise InvalidWorkflowOperation("Cannot archive the default workflow")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            status=WorkflowStatus.ARCHIVED,
            is_default=self.is_default,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def set_as_default(self) -> "CompanyWorkflow":
        """Set this workflow as the default for the company"""
        if self.status != WorkflowStatus.ACTIVE:
            raise InvalidWorkflowOperation("Only active workflows can be set as default")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            status=self.status,
            is_default=True,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def unset_as_default(self) -> "CompanyWorkflow":
        """Remove this workflow as the default"""
        if not self.is_default:
            raise InvalidWorkflowOperation("This workflow is not the default")

        return CompanyWorkflow(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            status=self.status,
            is_default=False,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
