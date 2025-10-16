from dataclasses import dataclass
from typing import Dict, Any

from src.job_position.domain.enums import JobPositionStatusEnum
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.query_bus import Query


@dataclass
class GetJobPositionsStatsQuery(Query):
    pass


class GetJobPositionsStatsQueryHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: GetJobPositionsStatsQuery) -> Dict[str, Any]:
        stats = {}

        # Count by status
        for status in JobPositionStatusEnum:
            stats[f"{status.value.lower()}_count"] = self.job_position_repository.count_by_status(status)

        # Total job positions
        stats["total_count"] = self.job_position_repository.count_total()

        # Recently created (last 30 days)
        stats["recent_count"] = self.job_position_repository.count_recent(days=30)

        return stats
