from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.company_bc.candidate_review.application.mappers.candidate_review_mapper import CandidateReviewMapper
from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class GetReviewByIdQuery(Query):
    """Query to get a candidate review by ID"""
    review_id: CandidateReviewId


class GetReviewByIdQueryHandler(QueryHandler[GetReviewByIdQuery, Optional[CandidateReviewDto]]):
    """Handler for getting candidate review by ID"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetReviewByIdQuery) -> Optional[CandidateReviewDto]:
        """Handle the get review by ID query"""
        review = self._repository.get_by_id(query.review_id)
        if not review:
            return None
        
        return CandidateReviewMapper.entity_to_dto(review)

