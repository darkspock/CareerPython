from dataclasses import dataclass
from typing import Dict, Any

from src.company_bc.company.domain.enums import CompanyStatusEnum
from src.company_bc.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetCompaniesStatsQuery(Query):
    pass


class GetCompaniesStatsQueryHandler(QueryHandler[GetCompaniesStatsQuery, Dict[str, Any]]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: GetCompaniesStatsQuery) -> Dict[str, Any]:
        stats = {}

        # Count by status
        for status in CompanyStatusEnum:
            stats[f"{status.value.lower()}_count"] = self.company_repository.count_by_status(status)

        # Total companies
        stats["total_count"] = self.company_repository.count_total()

        # Recently created (last 30 days)
        stats["recent_count"] = self.company_repository.count_recent(days=30)

        return stats
