from abc import ABC, abstractmethod
from typing import Optional, List

from src.company_workflow.domain.entities.company_workflow import CompanyWorkflow
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company.domain.value_objects.company_id import CompanyId


class CompanyWorkflowRepositoryInterface(ABC):
    """Repository interface for company workflow operations"""

    @abstractmethod
    def save(self, workflow: CompanyWorkflow) -> None:
        """Save a workflow"""
        pass

    @abstractmethod
    def get_by_id(self, workflow_id: CompanyWorkflowId) -> Optional[CompanyWorkflow]:
        """Get workflow by ID"""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[CompanyWorkflow]:
        """List all workflows for a company"""
        pass

    @abstractmethod
    def get_default_by_company(self, company_id: CompanyId) -> Optional[CompanyWorkflow]:
        """Get the default workflow for a company"""
        pass

    @abstractmethod
    def delete(self, workflow_id: CompanyWorkflowId) -> None:
        """Delete a workflow"""
        pass
