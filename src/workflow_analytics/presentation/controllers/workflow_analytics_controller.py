"""
Workflow Analytics Controller
Phase 9: HTTP controller for analytics endpoints
"""

from typing import List, Optional
from datetime import datetime

from src.shared.application.query_bus import QueryBus
from src.workflow_analytics.application.queries import (
    GetWorkflowAnalyticsQuery,
    GetStageBottlenecksQuery
)
from src.workflow_analytics.application.dtos import (
    WorkflowAnalyticsDto,
    StageBottleneckDto
)
from src.workflow_analytics.presentation.schemas import (
    WorkflowAnalyticsResponse,
    StageBottleneckResponse
)
from src.workflow_analytics.presentation.mappers import WorkflowAnalyticsMapper


class WorkflowAnalyticsController:
    """Controller for workflow analytics operations"""

    def __init__(self, query_bus: QueryBus):
        self._query_bus = query_bus

    def get_workflow_analytics(
        self,
        workflow_id: str,
        date_range_start: Optional[datetime] = None,
        date_range_end: Optional[datetime] = None
    ) -> WorkflowAnalyticsResponse:
        """
        Get comprehensive analytics for a workflow.

        Args:
            workflow_id: ID of the workflow to analyze
            date_range_start: Start date for filtering applications (optional)
            date_range_end: End date for filtering applications (optional)

        Returns:
            WorkflowAnalyticsResponse with complete analytics data

        Raises:
            ValueError: If workflow not found or has no stages
        """
        query = GetWorkflowAnalyticsQuery(
            workflow_id=workflow_id,
            date_range_start=date_range_start,
            date_range_end=date_range_end
        )

        dto: WorkflowAnalyticsDto = self._query_bus.query(query)
        return WorkflowAnalyticsMapper.analytics_to_response(dto)

    def get_stage_bottlenecks(
        self,
        workflow_id: str,
        date_range_start: Optional[datetime] = None,
        date_range_end: Optional[datetime] = None,
        min_bottleneck_score: float = 30.0
    ) -> List[StageBottleneckResponse]:
        """
        Get list of bottleneck stages in a workflow.

        Args:
            workflow_id: ID of the workflow to analyze
            date_range_start: Start date for filtering applications (optional)
            date_range_end: End date for filtering applications (optional)
            min_bottleneck_score: Minimum score to be considered a bottleneck (0-100)

        Returns:
            List of StageBottleneckResponse, sorted by score (worst first)

        Raises:
            ValueError: If workflow not found
        """
        query = GetStageBottlenecksQuery(
            workflow_id=workflow_id,
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            min_bottleneck_score=min_bottleneck_score
        )

        dtos: List[StageBottleneckDto] = self._query_bus.query(query)
        return WorkflowAnalyticsMapper.bottlenecks_to_response(dtos)
