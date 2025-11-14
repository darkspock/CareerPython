"""Get pending interviews by candidate and stage query"""
from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetPendingInterviewsByCandidateAndStageQuery(Query):
    candidate_id: str
    workflow_stage_id: str


class GetPendingInterviewsByCandidateAndStageQueryHandler(
    QueryHandler[GetPendingInterviewsByCandidateAndStageQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetPendingInterviewsByCandidateAndStageQuery) -> List[InterviewDto]:
        interviews = self.interview_repository.get_pending_interviews_by_candidate_and_stage(
            candidate_id=query.candidate_id,
            workflow_stage_id=query.workflow_stage_id
        )
        return [InterviewDto.from_entity(interview) for interview in interviews]
