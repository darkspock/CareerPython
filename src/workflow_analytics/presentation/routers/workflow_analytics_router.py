"""
Workflow Analytics Router
Phase 9: FastAPI routes for workflow analytics
"""

from typing import Annotated, List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from core.container import Container
from src.workflow_analytics.presentation.controllers import WorkflowAnalyticsController
from src.workflow_analytics.presentation.schemas import (
    WorkflowAnalyticsResponse,
    StageBottleneckResponse
)

router = APIRouter(
    prefix="/api/company/workflows",
    tags=["workflow-analytics"],
)


@router.get("/{workflow_id}/analytics", response_model=WorkflowAnalyticsResponse)
@inject
def get_workflow_analytics(
    workflow_id: str,
    date_range_start: Optional[datetime] = Query(None, description="Start date for filtering applications"),
    date_range_end: Optional[datetime] = Query(None, description="End date for filtering applications"),
    controller: Annotated[
        WorkflowAnalyticsController,
        Depends(Provide[Container.workflow_analytics_controller])
    ] = None,
) -> WorkflowAnalyticsResponse:
    """
    Get comprehensive analytics for a workflow.

    Returns:
    - Overall performance metrics (total, active, completed, rejected applications)
    - Per-stage analytics (conversion rates, time metrics, application counts)
    - Identified bottlenecks with scores and reasons
    - Summary insights (fastest/slowest stages, highest/lowest conversion)
    - Actionable recommendations

    Optional date range filters to analyze specific time periods.
    """
    return controller.get_workflow_analytics(
        workflow_id=workflow_id,
        date_range_start=date_range_start,
        date_range_end=date_range_end
    )


@router.get("/{workflow_id}/bottlenecks", response_model=List[StageBottleneckResponse])
@inject
def get_stage_bottlenecks(
    workflow_id: str,
    date_range_start: Optional[datetime] = Query(None, description="Start date for filtering applications"),
    date_range_end: Optional[datetime] = Query(None, description="End date for filtering applications"),
    min_bottleneck_score: float = Query(
        30.0,
        ge=0.0,
        le=100.0,
        description="Minimum score (0-100) to be considered a bottleneck"
    ),
    controller: Annotated[
        WorkflowAnalyticsController,
        Depends(Provide[Container.workflow_analytics_controller])
    ] = None,
) -> List[StageBottleneckResponse]:
    """
    Get list of bottleneck stages in a workflow.

    A stage is identified as a bottleneck based on:
    - Low conversion rate compared to average
    - High number of stuck applications
    - High dropout rate
    - Large volume of affected applications

    Returns stages sorted by bottleneck score (worst first).
    Only includes stages with score >= min_bottleneck_score.
    """
    return controller.get_stage_bottlenecks(
        workflow_id=workflow_id,
        date_range_start=date_range_start,
        date_range_end=date_range_end,
        min_bottleneck_score=min_bottleneck_score
    )
