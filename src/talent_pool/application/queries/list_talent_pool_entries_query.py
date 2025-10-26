"""
List Talent Pool Entries Query
Phase 8: Query to list talent pool entries for a company
"""

from dataclasses import dataclass
from typing import Optional, List

from src.shared.application.query_bus import QueryHandler, Query
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)
from src.talent_pool.application.dtos.talent_pool_entry_dto import TalentPoolEntryDto


@dataclass(frozen=True)
class ListTalentPoolEntriesQuery(Query):
    """Query to list talent pool entries for a company"""

    company_id: str
    status: Optional[TalentPoolStatus] = None
    tags: Optional[List[str]] = None
    min_rating: Optional[int] = None


class ListTalentPoolEntriesQueryHandler(QueryHandler[ListTalentPoolEntriesQuery, List[TalentPoolEntryDto]]):
    """Handler for list talent pool entries query"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListTalentPoolEntriesQuery) -> List[TalentPoolEntryDto]:
        """Execute the query to list talent pool entries"""
        entries = self._repository.list_by_company(
            company_id=query.company_id,
            status=query.status,
            tags=query.tags,
            min_rating=query.min_rating,
        )

        return [TalentPoolEntryDto.from_entity(entry) for entry in entries]
