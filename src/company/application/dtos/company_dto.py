from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.company.domain.enums import CompanyTypeEnum


@dataclass
class CompanyDto:
    """Company data transfer object"""
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
