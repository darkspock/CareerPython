from abc import ABC, abstractmethod
from typing import Optional, List

from src.workflow.domain.entities.workflow import Workflow
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.company.domain.value_objects.company_id import CompanyId


class WorkflowRepositoryInterface(ABC):
    """Repository interface for workflow operations"""

    @abstractmethod
    def save(self, workflow: Workflow) -> None:
        """Save or update a workflow"""
        pass

    @abstractmethod
    def get_by_id(self, workflow_id: WorkflowId) -> Optional[Workflow]:
        """Get a workflow by ID"""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[Workflow]:
        """Get all workflows for a company"""
        pass

    @abstractmethod
    def get_default_by_company(self, company_id: CompanyId) -> Optional[Workflow]:
        """Get the default workflow for a company"""
        pass

    @abstractmethod
    def delete(self, workflow_id: WorkflowId) -> None:
        """Delete a workflow"""
        pass

    @abstractmethod
    def list_by_phase_id(self, phase_id: str) -> List[Workflow]:
        """List all workflows for a phase"""
        pass

