"""
Get Workflow Analytics Query
Phase 9: Query for retrieving workflow analytics
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from typing import TYPE_CHECKING

from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow_analytics.application.dtos import (
    WorkflowAnalyticsDto,
    StageAnalyticsDto,
    StageBottleneckDto,
    WorkflowPerformanceDto
)

if TYPE_CHECKING:
    from core.database import SQLAlchemyDatabase


@dataclass
class GetWorkflowAnalyticsQuery(Query):
    """
    Query to get comprehensive analytics for a workflow.

    Analyzes application flow through workflow stages, calculates metrics,
    identifies bottlenecks, and provides recommendations.
    """
    workflow_id: str
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None


class GetWorkflowAnalyticsQueryHandler(QueryHandler[GetWorkflowAnalyticsQuery, WorkflowAnalyticsDto]):
    """Handler for GetWorkflowAnalyticsQuery"""

    def __init__(
            self,
            database: "SQLAlchemyDatabase",
            workflow_repository: WorkflowRepositoryInterface,
            stage_repository: WorkflowStageRepositoryInterface
    ):
        self._database = database
        self._workflow_repository = workflow_repository
        self._stage_repository = stage_repository

    def handle(self, query: GetWorkflowAnalyticsQuery) -> WorkflowAnalyticsDto:
        """Execute the query and return analytics"""
        # Get workflow entity
        workflow = self._workflow_repository.get_by_id(
            WorkflowId.from_string(query.workflow_id)
        )
        if not workflow:
            raise ValueError(f"Workflow {query.workflow_id} not found")

        # Get all stages for this workflow
        stages = self._stage_repository.list_by_workflow(workflow.id)
        if not stages:
            raise ValueError(f"No stages found for workflow {query.workflow_id}")

        # Calculate analytics using raw SQL for performance
        with self._database.get_session() as session:
            # Import models inline to avoid circular dependencies
            from src.company_bc.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel

            # Base query with date filtering
            base_query = session.query(CompanyCandidateModel).filter(
                CompanyCandidateModel.workflow_id == query.workflow_id
            )

            if query.date_range_start:
                base_query = base_query.filter(
                    CompanyCandidateModel.invited_at >= query.date_range_start
                )
            if query.date_range_end:
                base_query = base_query.filter(
                    CompanyCandidateModel.invited_at <= query.date_range_end
                )

            # Overall performance metrics
            total_applications = base_query.count()

            # Count by status
            from src.company_bc.company_candidate.domain.enums import CompanyCandidateStatus

            active_count = base_query.filter(
                CompanyCandidateModel.status.in_([
                    CompanyCandidateStatus.ACTIVE.value,
                    CompanyCandidateStatus.PENDING_CONFIRMATION.value
                ])
            ).count()

            completed_count = base_query.filter(
                CompanyCandidateModel.status == CompanyCandidateStatus.ACTIVE.value,
                CompanyCandidateModel.archived_at.isnot(None)
            ).count()

            rejected_count = base_query.filter(
                CompanyCandidateModel.status == CompanyCandidateStatus.REJECTED.value
            ).count()

            withdrawn_count = base_query.filter(
                CompanyCandidateModel.status == CompanyCandidateStatus.ARCHIVED.value
            ).count()

            # Applications per stage
            applications_per_stage: Dict[str, int] = {}
            for stage in stages:
                stage_count = base_query.filter(
                    CompanyCandidateModel.current_stage_id == str(stage.id)
                ).count()
                applications_per_stage[str(stage.id)] = stage_count

            # Calculate stage analytics
            stage_analytics_list: List[StageAnalyticsDto] = []

            for stage in stages:
                stage_id = str(stage.id)

                # Count applications in this stage
                current_in_stage = applications_per_stage.get(stage_id, 0)

                # For completed and rejected, we need to look at history
                # For now, we'll use simplified metrics based on current_stage_id
                # In a production system, you'd track stage history

                # Total that passed through this stage (current + moved on)
                total_in_stage = current_in_stage

                # For conversion rate, count how many moved to next stage
                next_stage_idx = stage.order + 1
                next_stages = [s for s in stages if s.order == next_stage_idx]

                moved_to_next = 0
                if next_stages:
                    for next_stage in next_stages:
                        moved_to_next += applications_per_stage.get(str(next_stage.id), 0)

                conversion_rate = None
                if total_in_stage > 0:
                    conversion_rate = (moved_to_next / total_in_stage) * 100

                dropout_rate = None
                if conversion_rate is not None:
                    dropout_rate = 100 - conversion_rate

                stage_analytics_list.append(StageAnalyticsDto(
                    stage_id=stage_id,
                    stage_name=stage.name,
                    stage_order=stage.order,
                    total_applications=total_in_stage,
                    current_applications=current_in_stage,
                    completed_applications=0,  # Would need stage history
                    rejected_applications=0,  # Would need stage history
                    average_time_hours=None,  # Would need timestamp tracking
                    median_time_hours=None,
                    min_time_hours=None,
                    max_time_hours=None,
                    conversion_rate_to_next=conversion_rate,
                    dropout_rate=dropout_rate
                ))

            # Create performance DTO
            performance = WorkflowPerformanceDto(
                workflow_id=query.workflow_id,
                workflow_name=workflow.name,
                total_applications=total_applications,
                active_applications=active_count,
                completed_applications=completed_count,
                rejected_applications=rejected_count,
                withdrawn_applications=withdrawn_count,
                average_completion_time_hours=None,  # Would need timestamp tracking
                median_completion_time_hours=None,
                overall_conversion_rate=None if total_applications == 0 else (
                                                                                         completed_count / total_applications) * 100,
                cost_per_hire=None,  # Would need cost tracking
                time_to_hire_days=None,  # Would need timestamp tracking
                applications_per_stage=applications_per_stage
            )

            # Identify bottlenecks
            bottlenecks = self._identify_bottlenecks(stage_analytics_list)

            # Generate insights
            fastest_stage = None
            slowest_stage = None
            highest_conversion = None
            lowest_conversion = None

            if stage_analytics_list:
                # Find stages with conversion data
                stages_with_conversion = [
                    s for s in stage_analytics_list
                    if s.conversion_rate_to_next is not None
                ]

                if stages_with_conversion:
                    highest_conversion_stage = max(
                        stages_with_conversion,
                        key=lambda s: s.conversion_rate_to_next or 0
                    )
                    highest_conversion = highest_conversion_stage.stage_name

                    lowest_conversion_stage = min(
                        stages_with_conversion,
                        key=lambda s: s.conversion_rate_to_next or 100
                    )
                    lowest_conversion = lowest_conversion_stage.stage_name

            # Generate recommendations
            recommendations = self._generate_recommendations(
                performance,
                stage_analytics_list,
                bottlenecks
            )

            # Create and return analytics DTO
            return WorkflowAnalyticsDto(
                workflow_id=query.workflow_id,
                workflow_name=workflow.name,
                company_id=str(workflow.company_id),
                analysis_date=datetime.utcnow(),
                date_range_start=query.date_range_start,
                date_range_end=query.date_range_end,
                performance=performance,
                stage_analytics=stage_analytics_list,
                bottlenecks=bottlenecks,
                total_stages=len(stages),
                fastest_stage=fastest_stage,
                slowest_stage=slowest_stage,
                highest_conversion_stage=highest_conversion,
                lowest_conversion_stage=lowest_conversion,
                recommendations=recommendations
            )

    def _identify_bottlenecks(
            self,
            stage_analytics: List[StageAnalyticsDto]
    ) -> List[StageBottleneckDto]:
        """
        Identify bottlenecks in the workflow.

        A stage is a bottleneck if:
        - Conversion rate is significantly below average
        - Has high number of current applications (stuck)
        """
        bottlenecks: List[StageBottleneckDto] = []

        # Calculate average conversion rate
        stages_with_conversion = [
            s for s in stage_analytics
            if s.conversion_rate_to_next is not None
        ]

        if not stages_with_conversion:
            return bottlenecks

        avg_conversion = sum(
            s.conversion_rate_to_next or 0.0 for s in stages_with_conversion
        ) / len(stages_with_conversion)

        # Expected conversion rate (we'll use average as baseline)
        expected_conversion = avg_conversion

        for stage in stage_analytics:
            if stage.conversion_rate_to_next is None:
                continue

            conversion_variance = (
                (stage.conversion_rate_to_next - expected_conversion) / expected_conversion * 100
                if expected_conversion > 0 else 0
            )

            # Calculate bottleneck score (0-100)
            # Higher score = worse bottleneck
            score = 0.0
            reasons = []

            # Low conversion rate
            if stage.conversion_rate_to_next < expected_conversion * 0.7:  # 30% below average
                score += 40
                reasons.append(
                    f"Low conversion rate ({stage.conversion_rate_to_next:.1f}% vs expected {expected_conversion:.1f}%)")

            # High number of stuck applications
            if stage.current_applications > stage.total_applications * 0.5:  # More than 50% stuck
                score += 30
                reasons.append(f"High number of stuck applications ({stage.current_applications})")

            # Very high dropout
            if stage.dropout_rate and stage.dropout_rate > 50:
                score += 30
                reasons.append(f"High dropout rate ({stage.dropout_rate:.1f}%)")

            # If score is significant, add as bottleneck
            if score >= 30:
                bottlenecks.append(StageBottleneckDto(
                    stage_id=stage.stage_id,
                    stage_name=stage.stage_name,
                    stage_order=stage.stage_order,
                    current_applications=stage.current_applications,
                    average_time_hours=stage.average_time_hours or 0,
                    expected_time_hours=0,  # Would need historical data
                    time_variance_percentage=0,
                    conversion_rate=stage.conversion_rate_to_next or 0,
                    expected_conversion_rate=expected_conversion,
                    conversion_variance_percentage=conversion_variance,
                    bottleneck_score=min(score, 100),
                    bottleneck_reasons=reasons
                ))

        # Sort by score (worst first)
        bottlenecks.sort(key=lambda b: b.bottleneck_score, reverse=True)

        return bottlenecks

    def _generate_recommendations(
            self,
            performance: WorkflowPerformanceDto,
            stage_analytics: List[StageAnalyticsDto],
            bottlenecks: List[StageBottleneckDto]
    ) -> List[str]:
        """Generate actionable recommendations based on analytics"""
        recommendations = []

        # Overall conversion
        if performance.overall_conversion_rate and performance.overall_conversion_rate < 20:
            recommendations.append(
                "Overall conversion rate is below 20%. Consider reviewing your candidate screening process."
            )

        # Bottlenecks
        if bottlenecks:
            for bottleneck in bottlenecks[:3]:  # Top 3 bottlenecks
                recommendations.append(
                    f"Focus on improving '{bottleneck.stage_name}' stage - {bottleneck.bottleneck_reasons[0]}"
                )

        # Stuck applications
        total_active = performance.active_applications
        if total_active > performance.total_applications * 0.7:
            recommendations.append(
                "More than 70% of applications are still active. Consider accelerating your review process."
            )

        # Stage-specific recommendations
        for stage in stage_analytics:
            if stage.current_applications > 50:  # Arbitrary threshold
                recommendations.append(
                    f"'{stage.stage_name}' has {stage.current_applications} pending applications. "
                    f"Consider adding reviewers or automating parts of this stage."
                )

        # If no specific issues found
        if not recommendations:
            recommendations.append(
                "Workflow is performing well. Continue monitoring conversion rates and application flow."
            )

        return recommendations
