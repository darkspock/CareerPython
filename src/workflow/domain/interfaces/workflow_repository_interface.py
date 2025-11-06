from abc import ABC, abstractmethod
from typing import Optional, List

from src.workflow.domain.entities.workflow import Workflow
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.phase.domain.value_objects.phase_id import PhaseId


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
    def list_by_company(self, company_id: CompanyId, workflow_type: Optional[WorkflowTypeEnum] = None) -> List[Workflow]:
        """Get all workflows for a company, optionally filtered by workflow_type"""
        pass

    @abstractmethod
    def get_default_by_company(self, company_id: CompanyId, workflow_type: Optional[WorkflowTypeEnum] = None) -> Optional[Workflow]:
        """Get the default workflow for a company, optionally filtered by workflow_type"""
        pass

    @abstractmethod
    def delete(self, workflow_id: WorkflowId) -> None:
        """Delete a workflow"""
        pass

    @abstractmethod
    def list_by_phase_id(self, phase_id: PhaseId, workflow_type: Optional[WorkflowTypeEnum] = None, status: Optional[str] = None) -> List[Workflow]:
        """List all workflows for a phase, optionally filtered by workflow_type and status"""
        pass

