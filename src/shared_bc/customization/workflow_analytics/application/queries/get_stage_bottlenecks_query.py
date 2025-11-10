"""
Get Stage Bottlenecks Query
Phase 9: Query for identifying workflow stage bottlenecks
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING, Dict, Any, cast

from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow_analytics.application.dtos import StageBottleneckDto

if TYPE_CHECKING:
    from core.database import SQLAlchemyDatabase


@dataclass
class GetStageBottlenecksQuery(Query):
    """
    Query to identify bottlenecks in a workflow's stages.

    Returns only stages that are identified as bottlenecks
    based on conversion rates and application flow.
    """
    workflow_id: str
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    min_bottleneck_score: float = 30.0  # Minimum score to be considered a bottleneck


class GetStageBottlenecksQueryHandler(QueryHandler[GetStageBottlenecksQuery, List[StageBottleneckDto]]):
    """Handler for GetStageBottlenecksQuery"""

    def __init__(
            self,
            database: "SQLAlchemyDatabase",
            workflow_repository: WorkflowRepositoryInterface,
            stage_repository: WorkflowStageRepositoryInterface
    ):
        self._database = database
        self._workflow_repository = workflow_repository
        self._stage_repository = stage_repository

    def handle(self, query: GetStageBottlenecksQuery) -> List[StageBottleneckDto]:
        """Execute the query and return bottlenecks"""
        # Verify workflow exists
        workflow = self._workflow_repository.get_by_id(
            WorkflowId.from_string(query.workflow_id)
        )
        if not workflow:
            raise ValueError(f"Workflow {query.workflow_id} not found")

        # Get all stages for this workflow
        stages = self._stage_repository.list_by_workflow(workflow.id)
        if not stages:
            return []

        bottlenecks: List[StageBottleneckDto] = []

        with self._database.get_session() as session:
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

            total_applications = base_query.count()

            if total_applications == 0:
                return []

            # Calculate metrics for each stage
            stage_metrics: List[Dict[str, Any]] = []

            for stage in stages:
                stage_id = str(stage.id)

                # Count current applications in this stage
                current_count = base_query.filter(
                    CompanyCandidateModel.current_stage_id == stage_id
                ).count()

                # For conversion, find next stage
                next_stage_idx = stage.order + 1
                next_stages = [s for s in stages if s.order == next_stage_idx]

                moved_to_next = 0
                if next_stages:
                    for next_stage in next_stages:
                        moved_to_next += base_query.filter(
                            CompanyCandidateModel.current_stage_id == str(next_stage.id)
                        ).count()

                # Calculate conversion rate
                total_in_stage = current_count + moved_to_next
                conversion_rate = 0.0
                if total_in_stage > 0:
                    conversion_rate = (moved_to_next / total_in_stage) * 100

                stage_metrics.append({
                    'stage': stage,
                    'stage_id': stage_id,
                    'current_count': current_count,
                    'total_count': total_in_stage,
                    'conversion_rate': conversion_rate
                })

            # Calculate average conversion rate
            stages_with_data = [m for m in stage_metrics if m['total_count'] > 0]
            if not stages_with_data:
                return []

            avg_conversion = sum(m['conversion_rate'] for m in stages_with_data) / len(stages_with_data)
            expected_conversion = avg_conversion

            # Identify bottlenecks
            for metric in stage_metrics:
                if cast(int, metric['total_count']) == 0:
                    continue

                from src.shared_bc.customization.workflow.domain.entities.workflow_stage import WorkflowStage
                stage = cast(WorkflowStage, metric['stage'])
                conversion_rate = cast(float, metric['conversion_rate'])
                current_count = cast(int, metric['current_count'])
                total_count = cast(int, metric['total_count'])

                # Calculate variance
                conversion_variance = 0.0
                if expected_conversion > 0:
                    conversion_variance = (
                            (conversion_rate - expected_conversion) / expected_conversion * 100
                    )

                # Calculate bottleneck score
                score = 0.0
                reasons = []

                # 1. Low conversion rate (40 points max)
                if conversion_rate < expected_conversion * 0.7:  # 30% below average
                    conversion_penalty = ((expected_conversion - conversion_rate) / expected_conversion) * 40
                    score += min(conversion_penalty, 40)
                    reasons.append(
                        f"Low conversion rate ({conversion_rate:.1f}% vs expected {expected_conversion:.1f}%)"
                    )

                # 2. High number of stuck applications (30 points max)
                stuck_percentage = (current_count / total_count) * 100
                if stuck_percentage > 50:
                    stuck_penalty = ((stuck_percentage - 50) / 50) * 30
                    score += min(stuck_penalty, 30)
                    reasons.append(
                        f"High number of stuck applications ({current_count} out of {total_count}, {stuck_percentage:.1f}%)"
                    )

                # 3. High dropout (30 points max)
                dropout_rate = 100 - conversion_rate
                if dropout_rate > 50:
                    dropout_penalty = ((dropout_rate - 50) / 50) * 30
                    score += min(dropout_penalty, 30)
                    reasons.append(f"High dropout rate ({dropout_rate:.1f}%)")

                # 4. Significant volume stuck (bonus points if many applications affected)
                if current_count >= 20:
                    score += 10
                    reasons.append(f"Large volume of applications affected ({current_count} applications)")

                # Only include if meets minimum score threshold
                if score >= query.min_bottleneck_score and reasons:
                    bottlenecks.append(StageBottleneckDto(
                        stage_id=cast(str, metric['stage_id']),
                        stage_name=stage.name,
                        stage_order=stage.order,
                        current_applications=current_count,
                        average_time_hours=0.0,  # Would need timestamp tracking
                        expected_time_hours=0.0,
                        time_variance_percentage=0.0,
                        conversion_rate=conversion_rate,
                        expected_conversion_rate=expected_conversion,
                        conversion_variance_percentage=conversion_variance,
                        bottleneck_score=min(score, 100),
                        bottleneck_reasons=reasons
                    ))

        # Sort by bottleneck score (worst first)
        bottlenecks.sort(key=lambda b: b.bottleneck_score, reverse=True)

        return bottlenecks
