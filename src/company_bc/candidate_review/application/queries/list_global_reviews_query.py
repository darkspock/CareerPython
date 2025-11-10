from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.company_bc.candidate_review.application.mappers.candidate_review_mapper import CandidateReviewMapper
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class ListGlobalReviewsQuery(Query):
    """Query to list all global reviews for a company candidate"""
    company_candidate_id: CompanyCandidateId


class ListGlobalReviewsQueryHandler(QueryHandler[ListGlobalReviewsQuery, List[CandidateReviewDto]]):
    """Handler for listing global candidate reviews"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListGlobalReviewsQuery) -> List[CandidateReviewDto]:
        """Handle the list global reviews query"""
        reviews = self._repository.get_global_reviews(query.company_candidate_id)
        
        return [CandidateReviewMapper.entity_to_dto(review) for review in reviews]

