"""
Workflow Analytics Mapper
Phase 9: Convert DTOs to Response schemas
"""

from typing import List

from src.shared_bc.customization.workflow_analytics.application.dtos import (
    WorkflowAnalyticsDto,
    StageAnalyticsDto,
    StageBottleneckDto,
    WorkflowPerformanceDto
)
from adapters.http.shared.workflow_analytics.schemas import (
    WorkflowAnalyticsResponse,
    StageAnalyticsResponse,
    StageBottleneckResponse,
    WorkflowPerformanceResponse
)


class WorkflowAnalyticsMapper:
    """Mapper for converting analytics DTOs to response schemas"""

    @staticmethod
    def stage_analytics_to_response(dto: StageAnalyticsDto) -> StageAnalyticsResponse:
        """Convert StageAnalyticsDto to StageAnalyticsResponse"""
        return StageAnalyticsResponse(
            stage_id=dto.stage_id,
            stage_name=dto.stage_name,
            stage_order=dto.stage_order,
            total_applications=dto.total_applications,
            current_applications=dto.current_applications,
            completed_applications=dto.completed_applications,
            rejected_applications=dto.rejected_applications,
            average_time_hours=dto.average_time_hours,
            median_time_hours=dto.median_time_hours,
            min_time_hours=dto.min_time_hours,
            max_time_hours=dto.max_time_hours,
            conversion_rate_to_next=dto.conversion_rate_to_next,
            dropout_rate=dto.dropout_rate
        )

    @staticmethod
    def bottleneck_to_response(dto: StageBottleneckDto) -> StageBottleneckResponse:
        """Convert StageBottleneckDto to StageBottleneckResponse"""
        return StageBottleneckResponse(
            stage_id=dto.stage_id,
            stage_name=dto.stage_name,
            stage_order=dto.stage_order,
            current_applications=dto.current_applications,
            average_time_hours=dto.average_time_hours,
            expected_time_hours=dto.expected_time_hours,
            time_variance_percentage=dto.time_variance_percentage,
            conversion_rate=dto.conversion_rate,
            expected_conversion_rate=dto.expected_conversion_rate,
            conversion_variance_percentage=dto.conversion_variance_percentage,
            bottleneck_score=dto.bottleneck_score,
            bottleneck_reasons=dto.bottleneck_reasons
        )

    @staticmethod
    def performance_to_response(dto: WorkflowPerformanceDto) -> WorkflowPerformanceResponse:
        """Convert WorkflowPerformanceDto to WorkflowPerformanceResponse"""
        return WorkflowPerformanceResponse(
            workflow_id=dto.workflow_id,
            workflow_name=dto.workflow_name,
            total_applications=dto.total_applications,
            active_applications=dto.active_applications,
            completed_applications=dto.completed_applications,
            rejected_applications=dto.rejected_applications,
            withdrawn_applications=dto.withdrawn_applications,
            average_completion_time_hours=dto.average_completion_time_hours,
            median_completion_time_hours=dto.median_completion_time_hours,
            overall_conversion_rate=dto.overall_conversion_rate,
            cost_per_hire=dto.cost_per_hire,
            time_to_hire_days=dto.time_to_hire_days,
            applications_per_stage=dto.applications_per_stage
        )

    @staticmethod
    def analytics_to_response(dto: WorkflowAnalyticsDto) -> WorkflowAnalyticsResponse:
        """Convert WorkflowAnalyticsDto to WorkflowAnalyticsResponse"""
        return WorkflowAnalyticsResponse(
            workflow_id=dto.workflow_id,
            workflow_name=dto.workflow_name,
            company_id=dto.company_id,
            analysis_date=dto.analysis_date,
            date_range_start=dto.date_range_start,
            date_range_end=dto.date_range_end,
            performance=WorkflowAnalyticsMapper.performance_to_response(dto.performance),
            stage_analytics=[
                WorkflowAnalyticsMapper.stage_analytics_to_response(stage)
                for stage in dto.stage_analytics
            ],
            bottlenecks=[
                WorkflowAnalyticsMapper.bottleneck_to_response(bottleneck)
                for bottleneck in dto.bottlenecks
            ],
            total_stages=dto.total_stages,
            fastest_stage=dto.fastest_stage,
            slowest_stage=dto.slowest_stage,
            highest_conversion_stage=dto.highest_conversion_stage,
            lowest_conversion_stage=dto.lowest_conversion_stage,
            recommendations=dto.recommendations
        )

    @staticmethod
    def bottlenecks_to_response(dtos: List[StageBottleneckDto]) -> List[StageBottleneckResponse]:
        """Convert list of StageBottleneckDto to list of StageBottleneckResponse"""
        return [
            WorkflowAnalyticsMapper.bottleneck_to_response(dto)
            for dto in dtos
        ]
