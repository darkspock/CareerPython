"""
Talent Pool Entry DTO
Phase 8: Data Transfer Object for talent pool entries
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.company_bc.talent_pool.domain.entities.talent_pool_entry import TalentPoolEntry
from src.company_bc.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus


@dataclass(frozen=True)
class TalentPoolEntryDto:
    """DTO for talent pool entry data transfer"""

    id: str
    company_id: str
    candidate_id: str
    source_application_id: Optional[str]
    source_position_id: Optional[str]
    added_reason: Optional[str]
    tags: List[str]
    rating: Optional[int]
    notes: Optional[str]
    status: TalentPoolStatus
    added_by_user_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: TalentPoolEntry) -> "TalentPoolEntryDto":
        """Create DTO from domain entity"""
        return TalentPoolEntryDto(
            id=str(entity.id),
            company_id=entity.company_id,
            candidate_id=entity.candidate_id,
            source_application_id=entity.source_application_id,
            source_position_id=entity.source_position_id,
            added_reason=entity.added_reason,
            tags=entity.tags,
            rating=entity.rating,
            notes=entity.notes,
            status=entity.status,
            added_by_user_id=entity.added_by_user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
