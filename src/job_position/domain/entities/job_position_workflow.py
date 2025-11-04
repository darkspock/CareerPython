from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.enums.workflow_type import WorkflowTypeEnum
from src.company.domain.value_objects.company_id import CompanyId


@dataclass
class JobPositionWorkflow:
    """
    Job Position Workflow entity.
    
    Represents a workflow configuration for managing job positions through stages.
    Each workflow has stages that map to JobPositionStatusEnum values.
    """
    id: JobPositionWorkflowId
    company_id: CompanyId
    name: str
    workflow_type: WorkflowTypeEnum
    default_view: ViewTypeEnum
    stages: List[WorkflowStage]
    custom_fields_config: Dict[str, Any]  # JSON configuration for custom fields
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: JobPositionWorkflowId,
        company_id: CompanyId,
        name: str,
        workflow_type: WorkflowTypeEnum = WorkflowTypeEnum.STANDARD,
        default_view: ViewTypeEnum = ViewTypeEnum.KANBAN,
        stages: Optional[List[WorkflowStage]] = None,
        custom_fields_config: Optional[Dict[str, Any]] = None,
    ) -> "JobPositionWorkflow":
        """
        Factory method to create a new JobPositionWorkflow
        
        Args:
            id: Workflow ID
            company_id: Company ID
            name: Workflow name
            workflow_type: Type of workflow
            default_view: Default view type
            stages: List of stages (optional, can be added later)
            custom_fields_config: Custom fields configuration
            
        Returns:
            JobPositionWorkflow: New instance
            
        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Workflow name cannot be empty")
        
        now = datetime.utcnow()
        return cls(
            id=id,
            company_id=company_id,
            name=name.strip(),
            workflow_type=workflow_type,
            default_view=default_view,
            stages=stages or [],
            custom_fields_config=custom_fields_config or {},
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        name: str,
        workflow_type: Optional[WorkflowTypeEnum] = None,
        default_view: Optional[ViewTypeEnum] = None,
        custom_fields_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update workflow information
        
        Args:
            name: New workflow name
            workflow_type: New workflow type (optional)
            default_view: New default view (optional)
            custom_fields_config: New custom fields config (optional)
            
        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Workflow name cannot be empty")
        
        self.name = name.strip()
        if workflow_type is not None:
            self.workflow_type = workflow_type
        if default_view is not None:
            self.default_view = default_view
        if custom_fields_config is not None:
            self.custom_fields_config = custom_fields_config
        self.updated_at = datetime.utcnow()

    def add_stage(self, stage: WorkflowStage) -> None:
        """
        Add a stage to the workflow
        
        Args:
            stage: Stage to add
            
        Raises:
            ValueError: If stage with same ID already exists
        """
        if any(s.id.value == stage.id.value for s in self.stages):
            raise ValueError(f"Stage with ID {stage.id.value} already exists in workflow")
        
        self.stages.append(stage)
        self.updated_at = datetime.utcnow()

    def remove_stage(self, stage_id: str) -> None:
        """
        Remove a stage from the workflow
        
        Args:
            stage_id: ID of stage to remove
            
        Raises:
            ValueError: If stage not found
        """
        initial_count = len(self.stages)
        self.stages = [s for s in self.stages if s.id.value != stage_id]
        
        if len(self.stages) == initial_count:
            raise ValueError(f"Stage with ID {stage_id} not found in workflow")
        
        self.updated_at = datetime.utcnow()

    def update_stage(self, stage_id: str, updated_stage: WorkflowStage) -> None:
        """
        Update a stage in the workflow
        
        Args:
            stage_id: ID of stage to update
            updated_stage: Updated stage (must have same ID)
            
        Raises:
            ValueError: If stage not found or IDs don't match
        """
        if stage_id != updated_stage.id.value:
            raise ValueError("Stage ID mismatch")
        
        for i, stage in enumerate(self.stages):
            if stage.id.value == stage_id:
                self.stages[i] = updated_stage
                self.updated_at = datetime.utcnow()
                return
        
        raise ValueError(f"Stage with ID {stage_id} not found in workflow")

    def get_stage_by_id(self, stage_id: str) -> Optional[WorkflowStage]:
        """
        Get a stage by ID
        
        Args:
            stage_id: Stage ID to find
            
        Returns:
            WorkflowStage if found, None otherwise
        """
        for stage in self.stages:
            if stage.id.value == stage_id:
                return stage
        return None

