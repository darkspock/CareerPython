from abc import ABC, abstractmethod
from typing import Optional, List

from src.workflow.domain.entities.workflow_stage import WorkflowStage
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.phase.domain.value_objects.phase_id import PhaseId


class WorkflowStageRepositoryInterface(ABC):
    """Repository interface for workflow stage operations"""

    @abstractmethod
    def save(self, stage: WorkflowStage) -> None:
        """Save or update a workflow stage"""
        pass

    @abstractmethod
    def get_by_id(self, stage_id: WorkflowStageId) -> Optional[WorkflowStage]:
        """Get stage by ID"""
        pass

    @abstractmethod
    def list_by_workflow(self, workflow_id: WorkflowId) -> List[WorkflowStage]:
        """List all stages for a workflow, ordered by order field"""
        pass

    @abstractmethod
    def delete(self, stage_id: WorkflowStageId) -> None:
        """Delete a stage"""
        pass

    @abstractmethod
    def get_initial_stage(self, workflow_id: WorkflowId) -> Optional[WorkflowStage]:
        """Get the initial stage of a workflow"""
        pass

    @abstractmethod
    def get_final_stages(self, workflow_id: WorkflowId) -> List[WorkflowStage]:
        """Get all final stages of a workflow (SUCCESS and FAIL stages)"""
        pass

    @abstractmethod
    def list_by_phase(self, phase_id: PhaseId) -> List[WorkflowStage]:
        """List all stages for a phase, ordered by order field"""
        pass

