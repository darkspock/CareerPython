"""Job position workflow DTOs"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.job_position.domain.entities.job_position_workflow import JobPositionWorkflow
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.company.domain.value_objects.company_id import CompanyId


@dataclass
class WorkflowStageDto:
    """DTO for workflow stage"""
    id: str
    name: str
    icon: str
    background_color: str
    text_color: str
    role: Optional[str]  # CompanyRoleId as string
    status_mapping: str  # JobPositionStatusEnum value
    kanban_display: str  # KanbanDisplayEnum value
    field_visibility: Dict[str, bool]
    field_validation: Dict[str, Any]
    field_candidate_visibility: Dict[str, bool]  # Field visibility for candidates

    @staticmethod
    def from_value_object(stage: WorkflowStage) -> 'WorkflowStageDto':
        """Create DTO from WorkflowStage value object"""
        return WorkflowStageDto(
            id=stage.id.value,
            name=stage.name,
            icon=stage.icon,
            background_color=stage.background_color,
            text_color=stage.text_color,
            role=stage.role.value if stage.role else None,
            status_mapping=stage.status_mapping.value,
            kanban_display=stage.kanban_display.value,
            field_visibility=stage.field_visibility,
            field_validation=stage.field_validation,
            field_candidate_visibility=stage.field_candidate_visibility,
        )


@dataclass
class JobPositionWorkflowDto:
    """DTO for job position workflow"""
    id: str
    company_id: str
    name: str
    default_view: str
    stages: List[WorkflowStageDto]
    custom_fields_config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: JobPositionWorkflow) -> 'JobPositionWorkflowDto':
        """Create DTO from JobPositionWorkflow entity"""
        return JobPositionWorkflowDto(
            id=entity.id.value,
            company_id=entity.company_id.value,
            name=entity.name,
            default_view=entity.default_view.value,
            stages=[WorkflowStageDto.from_value_object(stage) for stage in entity.stages],
            custom_fields_config=entity.custom_fields_config,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

