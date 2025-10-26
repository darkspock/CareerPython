"""
Search Talent Pool Query
Phase 8: Query to search talent pool entries
"""

from dataclasses import dataclass
from typing import Optional, List

from src.shared.application.query_bus import QueryHandler, Query
from src.talent_pool.application.dtos.talent_pool_entry_dto import TalentPoolEntryDto
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)


@dataclass(frozen=True)
class SearchTalentPoolQuery(Query):
    """Query to search talent pool entries"""

    company_id: str
    search_term: Optional[str] = None
    status: Optional[TalentPoolStatus] = None
    tags: Optional[List[str]] = None
    min_rating: Optional[int] = None


class SearchTalentPoolQueryHandler(QueryHandler[SearchTalentPoolQuery, List[TalentPoolEntryDto]]):
    """Handler for search talent pool query"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def handle(self, query: SearchTalentPoolQuery) -> List[TalentPoolEntryDto]:
        """Execute the query to search talent pool entries"""
        entries = self._repository.search(
            company_id=query.company_id,
            search_term=query.search_term,
            status=query.status,
            tags=query.tags,
            min_rating=query.min_rating,
        )

        return [TalentPoolEntryDto.from_entity(entry) for entry in entries]
