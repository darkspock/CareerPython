"""Job position workflow admin schemas"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.enums.job_position_status import JobPositionStatusEnum
from src.job_position.domain.enums.kanban_display import KanbanDisplayEnum


class WorkflowStageCreate(BaseModel):
    """Schema for creating a workflow stage"""
    id: str = Field(..., description="Stage ID")
    name: str = Field(..., description="Stage name")
    icon: str = Field(..., description="Stage icon")
    background_color: str = Field(..., description="Background color")
    text_color: str = Field(..., description="Text color")
    role: Optional[str] = Field(None, description="Responsible role ID")
    status_mapping: str = Field(..., description="Status mapping (JobPositionStatusEnum value)")
    kanban_display: str = Field("vertical", description="Kanban display type")
    field_visibility: Dict[str, bool] = Field(default_factory=dict, description="Field visibility configuration")
    field_validation: Dict[str, Any] = Field(default_factory=dict, description="Field validation configuration")


class WorkflowStageResponse(BaseModel):
    """Schema for workflow stage response"""
    id: str
    name: str
    icon: str
    background_color: str
    text_color: str
    role: Optional[str]
    status_mapping: str
    kanban_display: str
    field_visibility: Dict[str, bool]
    field_validation: Dict[str, Any]


class JobPositionWorkflowCreate(BaseModel):
    """Schema for creating a job position workflow"""
    company_id: str = Field(..., description="Company ID")
    name: str = Field(..., description="Workflow name")
    default_view: str = Field("kanban", description="Default view type")
    stages: List[WorkflowStageCreate] = Field(default_factory=list, description="Workflow stages")
    custom_fields_config: Dict[str, Any] = Field(default_factory=dict, description="Custom fields configuration")


class JobPositionWorkflowUpdate(BaseModel):
    """Schema for updating a job position workflow"""
    name: str = Field(..., description="Workflow name")
    default_view: Optional[str] = Field(None, description="Default view type")
    stages: Optional[List[WorkflowStageCreate]] = Field(None, description="Workflow stages")
    custom_fields_config: Optional[Dict[str, Any]] = Field(None, description="Custom fields configuration")


class JobPositionWorkflowResponse(BaseModel):
    """Schema for job position workflow response"""
    id: str
    company_id: str
    name: str
    default_view: str
    stages: List[WorkflowStageResponse]
    custom_fields_config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class MoveJobPositionToStageRequest(BaseModel):
    """Schema for moving a job position to a new stage"""
    stage_id: str = Field(..., description="New stage ID")
    comment: Optional[str] = Field(None, description="Optional comment for the stage change")


class UpdateJobPositionCustomFieldsRequest(BaseModel):
    """Schema for updating custom fields values"""
    custom_fields_values: Dict[str, Any] = Field(..., description="Custom fields values")

