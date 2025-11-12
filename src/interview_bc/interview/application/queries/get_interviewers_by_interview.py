"""Get interviewers by interview query"""
from dataclasses import dataclass
from typing import List

from src.interview_bc.interview.application.queries.dtos.interview_interviewer_dto import InterviewInterviewerDto
from src.interview_bc.interview.domain.infrastructure.interview_interviewer_repository_interface import \
    InterviewInterviewerRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewersByInterviewQuery(Query):
    interview_id: str


class GetInterviewersByInterviewQueryHandler(QueryHandler[GetInterviewersByInterviewQuery, List[InterviewInterviewerDto]]):
    def __init__(self, interviewer_repository: InterviewInterviewerRepositoryInterface):
        self.interviewer_repository = interviewer_repository

    def handle(self, query: GetInterviewersByInterviewQuery) -> List[InterviewInterviewerDto]:
        """Get all interviewers for an interview"""
        interviewers = self.interviewer_repository.get_by_interview_id(query.interview_id)
        return [InterviewInterviewerDto.from_entity(interviewer) for interviewer in interviewers]

