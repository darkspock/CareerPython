"""Company Role DTO."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CompanyRoleDto:
    """DTO for company role."""
    id: str
    company_id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
