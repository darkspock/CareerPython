"""Company DTO for application layer"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.company.domain.entities.company import Company
from src.company.domain.value_objects.company_id import CompanyId
from src.user.domain.value_objects.UserId import UserId


@dataclass
class CompanyDto:
    """Data transfer object for Company"""
    id: CompanyId
    name: str
    user_id: Optional[UserId]
    created_at: datetime
    updated_at: datetime
    sector: Optional[str] = None
    size: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None
    status: str = "PENDING"

    @classmethod
    def from_entity(cls, company: Company) -> "CompanyDto":
        """Convert Company entity to DTO"""
        return cls(
            id=company.id,
            name=company.name,
            user_id=company.user_id,
            created_at=company.created_at,
            updated_at=company.updated_at,
            sector=company.sector,
            size=company.size,
            location=company.location,
            website=company.website,
            culture=company.culture,
            external_data=company.external_data,
            status=company.status.value
        )


@dataclass
class CompanyStatsDto:
    """Company statistics DTO"""
    total_companies: int
    pending_approval: int
    approved_companies: int
    active_companies: int
    rejected_companies: int

    @classmethod
    def create(
            cls,
            total_companies: int = 0,
            pending_approval: int = 0,
            approved_companies: int = 0,
            active_companies: int = 0,
            rejected_companies: int = 0
    ) -> "CompanyStatsDto":
        return cls(
            total_companies=total_companies,
            pending_approval=pending_approval,
            approved_companies=approved_companies,
            active_companies=active_companies,
            rejected_companies=rejected_companies
        )
