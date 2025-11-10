"""Company DTO for application layer"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.company_bc.company.domain.entities.company import Company
from src.company_bc.company.domain.enums import CompanyTypeEnum


@dataclass
class CompanyDto:
    """Data transfer object for Company"""
    id: str
    name: str
    domain: str
    slug: Optional[str]
    logo_url: Optional[str]
    settings: Dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime
    company_type: Optional[CompanyTypeEnum] = None

    @classmethod
    def from_entity(cls, company: Company) -> "CompanyDto":
        """Convert Company entity to DTO"""
        return cls(
            id=str(company.id),
            name=company.name,
            domain=company.domain,
            slug=company.slug,
            logo_url=company.logo_url,
            settings=company.settings.to_dict(),
            status=company.status.value if hasattr(company.status, 'value') else company.status,
            created_at=company.created_at,
            updated_at=company.updated_at,
            company_type=company.company_type
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
