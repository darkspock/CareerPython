from dataclasses import dataclass
from typing import Dict, Any

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetResumeStatisticsQuery(Query):
    """Query to get resume statistics"""
    candidate_id: CandidateId


class GetResumeStatisticsQueryHandler(QueryHandler[GetResumeStatisticsQuery, Dict[str, Any]]):
    """Handler to get resume statistics"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def handle(self, query: GetResumeStatisticsQuery) -> Dict[str, Any]:
        """Handle resume statistics query"""

        # Get statistics from repository
        return self.resume_repository.get_statistics_by_candidate(query.candidate_id)
