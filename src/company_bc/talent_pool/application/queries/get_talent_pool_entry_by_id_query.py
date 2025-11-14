"""
Get Talent Pool Entry By ID Query
Phase 8: Query to get a talent pool entry by ID
"""

from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId
from src.company_bc.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)
from src.company_bc.talent_pool.application.dtos.talent_pool_entry_dto import TalentPoolEntryDto


@dataclass(frozen=True)
class GetTalentPoolEntryByIdQuery(Query):
    """Query to get a talent pool entry by ID"""

    entry_id: str


class GetTalentPoolEntryByIdQueryHandler(QueryHandler[GetTalentPoolEntryByIdQuery, Optional[TalentPoolEntryDto]]):
    """Handler for get talent pool entry by ID query"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetTalentPoolEntryByIdQuery) -> Optional[TalentPoolEntryDto]:
        """Execute the query to get talent pool entry by ID"""
        entry_id = TalentPoolEntryId.from_string(query.entry_id)
        entry = self._repository.get_by_id(entry_id)

        if not entry:
            return None

        return TalentPoolEntryDto.from_entity(entry)
