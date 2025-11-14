"""
Workflow Analytics DTOs
Phase 9: DTOs for workflow analytics data
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict


@dataclass
class StageAnalyticsDto:
    """
    Analytics data for a single workflow stage.

    Provides metrics on application flow through a specific stage.
    """
    stage_id: str
    stage_name: str
    stage_order: int
    total_applications: int
    current_applications: int
    completed_applications: int
    rejected_applications: int
    average_time_hours: Optional[float]
    median_time_hours: Optional[float]
    min_time_hours: Optional[float]
    max_time_hours: Optional[float]
    conversion_rate_to_next: Optional[float]  # Percentage (0-100)
    dropout_rate: Optional[float]  # Percentage (0-100)


@dataclass
class StageBottleneckDto:
    """
    Identifies bottlenecks in workflow stages.

    A bottleneck is a stage where applications spend significantly
    more time than expected or have lower conversion rates.
    """
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
    bottleneck_score: float  # 0-100, higher = worse bottleneck
    bottleneck_reasons: List[str]


@dataclass
class WorkflowPerformanceDto:
    """
    Overall performance metrics for a workflow.

    Provides high-level KPIs for workflow efficiency.
    """
    workflow_id: str
    workflow_name: str
    total_applications: int
    active_applications: int
    completed_applications: int
    rejected_applications: int
    withdrawn_applications: int
    average_completion_time_hours: Optional[float]
    median_completion_time_hours: Optional[float]
    overall_conversion_rate: Optional[float]  # Start to finish percentage
    cost_per_hire: Optional[float]
    time_to_hire_days: Optional[float]
    applications_per_stage: Dict[str, int]  # stage_id -> count


@dataclass
class WorkflowAnalyticsDto:
    """
    Complete analytics data for a workflow.

    Combines performance metrics, stage analytics, and bottleneck identification.
    """
    workflow_id: str
    workflow_name: str
    company_id: str
    analysis_date: datetime
    date_range_start: Optional[datetime]
    date_range_end: Optional[datetime]

    # Overall performance
    performance: WorkflowPerformanceDto

    # Per-stage analytics
    stage_analytics: List[StageAnalyticsDto]

    # Identified bottlenecks
    bottlenecks: List[StageBottleneckDto]

    # Summary insights
    total_stages: int
    fastest_stage: Optional[str]  # Stage name
    slowest_stage: Optional[str]  # Stage name
    highest_conversion_stage: Optional[str]
    lowest_conversion_stage: Optional[str]

    # Recommendations
    recommendations: List[str]
