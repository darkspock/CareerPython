from abc import ABC, abstractmethod
from typing import Optional, List

from src.job_position.domain.entities.job_position_workflow import JobPositionWorkflow
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.enums.workflow_type import WorkflowTypeEnum


class JobPositionWorkflowRepositoryInterface(ABC):
    """Job position workflow repository interface"""

    @abstractmethod
    def save(self, workflow: JobPositionWorkflow) -> None:
        """Save or update a workflow"""
        pass

    @abstractmethod
    def get_by_id(self, workflow_id: JobPositionWorkflowId) -> Optional[JobPositionWorkflow]:
        """Get a workflow by ID"""
        pass

    @abstractmethod
    def get_by_company_id(self, company_id: CompanyId) -> List[JobPositionWorkflow]:
        """Get all workflows for a company"""
        pass

    @abstractmethod
    def get_by_company_and_type(
        self,
        company_id: CompanyId,
        workflow_type: WorkflowTypeEnum
    ) -> List[JobPositionWorkflow]:
        """Get workflows by company and type"""
        pass

    @abstractmethod
    def delete(self, workflow_id: JobPositionWorkflowId) -> None:
        """Delete a workflow"""
        pass

