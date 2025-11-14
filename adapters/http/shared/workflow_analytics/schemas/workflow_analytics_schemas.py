"""
Workflow Analytics Response Schemas
Phase 9: Pydantic schemas for API responses
"""

from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class StageAnalyticsResponse(BaseModel):
    """Response schema for stage analytics"""
    stage_id: str
    stage_name: str
    stage_order: int
    total_applications: int
    current_applications: int
    completed_applications: int
    rejected_applications: int
    average_time_hours: Optional[float] = None
    median_time_hours: Optional[float] = None
    min_time_hours: Optional[float] = None
    max_time_hours: Optional[float] = None
    conversion_rate_to_next: Optional[float] = Field(None, description="Percentage (0-100)")
    dropout_rate: Optional[float] = Field(None, description="Percentage (0-100)")

    class Config:
        from_attributes = True


class StageBottleneckResponse(BaseModel):
    """Response schema for stage bottleneck"""
    stage_id: str
    stage_name: str
    stage_order: int
    current_applications: int
    average_time_hours: float
    expected_time_hours: float
    time_variance_percentage: float
    conversion_rate: float
    expected_conversion_rate: float
    conversion_variance_percentage: float
    bottleneck_score: float = Field(..., description="0-100, higher = worse bottleneck")
    bottleneck_reasons: List[str]

    class Config:
        from_attributes = True


class WorkflowPerformanceResponse(BaseModel):
    """Response schema for workflow performance"""
    workflow_id: str
    workflow_name: str
    total_applications: int
    active_applications: int
    completed_applications: int
    rejected_applications: int
    withdrawn_applications: int
    average_completion_time_hours: Optional[float] = None
    median_completion_time_hours: Optional[float] = None
    overall_conversion_rate: Optional[float] = Field(None, description="Percentage (0-100)")
    cost_per_hire: Optional[float] = None
    time_to_hire_days: Optional[float] = None
    applications_per_stage: Dict[str, int]

    class Config:
        from_attributes = True


class WorkflowAnalyticsResponse(BaseModel):
    """Response schema for complete workflow analytics"""
    workflow_id: str
    workflow_name: str
    company_id: str
    analysis_date: datetime
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None

    # Overall performance
    performance: WorkflowPerformanceResponse

    # Per-stage analytics
    stage_analytics: List[StageAnalyticsResponse]

    # Identified bottlenecks
    bottlenecks: List[StageBottleneckResponse]

    # Summary insights
    total_stages: int
    fastest_stage: Optional[str] = None
    slowest_stage: Optional[str] = None
    highest_conversion_stage: Optional[str] = None
    lowest_conversion_stage: Optional[str] = None

    # Recommendations
    recommendations: List[str]

    class Config:
        from_attributes = True
