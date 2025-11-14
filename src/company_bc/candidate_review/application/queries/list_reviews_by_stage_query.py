from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.company_bc.candidate_review.application.mappers.candidate_review_mapper import CandidateReviewMapper
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class ListReviewsByStageQuery(Query):
    """Query to list all reviews for a company candidate in a specific stage"""
    company_candidate_id: CompanyCandidateId
    stage_id: WorkflowStageId


class ListReviewsByStageQueryHandler(QueryHandler[ListReviewsByStageQuery, List[CandidateReviewDto]]):
    """Handler for listing candidate reviews by stage"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListReviewsByStageQuery) -> List[CandidateReviewDto]:
        """Handle the list reviews by stage query"""
        reviews = self._repository.get_by_stage(
            query.company_candidate_id,
            query.stage_id
        )
        
        return [CandidateReviewMapper.entity_to_dto(review) for review in reviews]

