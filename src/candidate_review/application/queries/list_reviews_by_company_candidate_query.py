from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query, QueryHandler
from src.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.candidate_review.application.mappers.candidate_review_mapper import CandidateReviewMapper
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class ListReviewsByCompanyCandidateQuery(Query):
    """Query to list all reviews for a company candidate"""
    company_candidate_id: CompanyCandidateId


class ListReviewsByCompanyCandidateQueryHandler(QueryHandler[ListReviewsByCompanyCandidateQuery, List[CandidateReviewDto]]):
    """Handler for listing candidate reviews by company candidate"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListReviewsByCompanyCandidateQuery) -> List[CandidateReviewDto]:
        """Handle the list reviews by company candidate query"""
        reviews = self._repository.get_by_company_candidate(query.company_candidate_id)
        
        return [CandidateReviewMapper.entity_to_dto(review) for review in reviews]

