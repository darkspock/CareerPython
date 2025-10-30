from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query, QueryHandler
from src.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto
from src.company_candidate.application.mappers.candidate_comment_mapper import CandidateCommentMapper
from src.company_candidate.domain.value_objects import CompanyCandidateId
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import CandidateCommentRepositoryInterface


@dataclass(frozen=True)
class ListCandidateCommentsByCompanyCandidateQuery(Query):
    """Query to list all comments for a company candidate"""
    company_candidate_id: str


class ListCandidateCommentsByCompanyCandidateQueryHandler(QueryHandler[ListCandidateCommentsByCompanyCandidateQuery, List[CandidateCommentDto]]):
    """Handler for listing candidate comments by company candidate"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCandidateCommentsByCompanyCandidateQuery) -> List[CandidateCommentDto]:
        """Handle the list candidate comments by company candidate query"""
        comments = self._repository.list_by_company_candidate(
            CompanyCandidateId.from_string(query.company_candidate_id)
        )
        
        return [CandidateCommentMapper.entity_to_dto(comment) for comment in comments]

