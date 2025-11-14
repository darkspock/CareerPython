from dataclasses import dataclass
from typing import List

from src.company_bc.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto
from src.company_bc.company_candidate.application.mappers.candidate_comment_mapper import CandidateCommentMapper
from src.company_bc.company_candidate.domain.infrastructure.candidate_comment_repository_interface import \
    CandidateCommentRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects import CompanyCandidateId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class ListCandidateCommentsByStageQuery(Query):
    """Query to list all comments for a company candidate in a specific stage"""
    company_candidate_id: str
    stage_id: str


class ListCandidateCommentsByStageQueryHandler(
    QueryHandler[ListCandidateCommentsByStageQuery, List[CandidateCommentDto]]):
    """Handler for listing candidate comments by stage"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCandidateCommentsByStageQuery) -> List[CandidateCommentDto]:
        """Handle the list candidate comments by stage query"""
        comments = self._repository.list_by_stage(
            CompanyCandidateId.from_string(query.company_candidate_id),
            WorkflowStageId.from_string(query.stage_id)
        )

        return [CandidateCommentMapper.entity_to_dto(comment) for comment in comments]
