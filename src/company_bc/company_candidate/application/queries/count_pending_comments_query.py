from dataclasses import dataclass

from src.company_bc.company_candidate.domain.infrastructure.candidate_comment_repository_interface import \
    CandidateCommentRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects import CompanyCandidateId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class CountPendingCommentsQuery(Query):
    """Query to count pending comments for a company candidate"""
    company_candidate_id: str


class CountPendingCommentsQueryHandler(QueryHandler[CountPendingCommentsQuery, int]):
    """Handler for counting pending comments"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def handle(self, query: CountPendingCommentsQuery) -> int:
        """Handle the count pending comments query"""
        return self._repository.count_pending_by_company_candidate(
            CompanyCandidateId.from_string(query.company_candidate_id)
        )
