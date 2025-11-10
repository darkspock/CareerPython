from dataclasses import dataclass
from typing import Dict, Any

from src.candidate_bc.candidate.domain.enums import CandidateStatusEnum
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.framework.application.query_bus import Query


@dataclass
class GetCandidatesStatsQuery(Query):
    pass


class GetCandidatesStatsQueryHandler:
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def execute(self, query: GetCandidatesStatsQuery) -> Dict[str, Any]:
        stats = {}

        # Count by status
        for status in CandidateStatusEnum:
            stats[f"{status.value.lower()}_count"] = self.candidate_repository.count_by_status(status)

        # Total candidates
        stats["total_count"] = self.candidate_repository.count_total()

        # Recently created (last 30 days)
        stats["recent_count"] = self.candidate_repository.count_recent(days=30)

        # Candidates with resume
        stats["with_resume_count"] = self.candidate_repository.count_with_resume()

        # Active candidates (not inactive)
        stats["active_count"] = self.candidate_repository.count_active()

        return stats
