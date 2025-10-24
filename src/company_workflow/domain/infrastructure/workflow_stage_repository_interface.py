from abc import ABC, abstractmethod
from typing import Optional, List

from src.company_workflow.domain.entities.workflow_stage import WorkflowStage
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId


class WorkflowStageRepositoryInterface(ABC):
    """Repository interface for workflow stage operations"""

    @abstractmethod
    def save(self, stage: WorkflowStage) -> None:
        """Save a workflow stage"""
        pass

    @abstractmethod
    def get_by_id(self, stage_id: WorkflowStageId) -> Optional[WorkflowStage]:
        """Get stage by ID"""
        pass

    @abstractmethod
    def list_by_workflow(self, workflow_id: CompanyWorkflowId) -> List[WorkflowStage]:
        """List all stages for a workflow, ordered by order field"""
        pass

    @abstractmethod
    def delete(self, stage_id: WorkflowStageId) -> None:
        """Delete a stage"""
        pass

    @abstractmethod
    def get_initial_stage(self, workflow_id: CompanyWorkflowId) -> Optional[WorkflowStage]:
        """Get the initial stage of a workflow"""
        pass

    @abstractmethod
    def get_final_stages(self, workflow_id: CompanyWorkflowId) -> List[WorkflowStage]:
        """Get all final stages of a workflow"""
        pass
