from dataclasses import dataclass
from typing import Optional

from src.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto
from src.company_candidate.application.mappers.candidate_comment_mapper import CandidateCommentMapper
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import \
    CandidateCommentRepositoryInterface
from src.company_candidate.domain.value_objects import CandidateCommentId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetCandidateCommentByIdQuery(Query):
    """Query to get a candidate comment by ID"""
    id: str


class GetCandidateCommentByIdQueryHandler(QueryHandler[GetCandidateCommentByIdQuery, Optional[CandidateCommentDto]]):
    """Handler for getting candidate comment by ID"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCandidateCommentByIdQuery) -> Optional[CandidateCommentDto]:
        """Handle the get candidate comment by ID query"""
        comment = self._repository.get_by_id(CandidateCommentId.from_string(query.id))
        if not comment:
            return None

        return CandidateCommentMapper.entity_to_dto(comment)
