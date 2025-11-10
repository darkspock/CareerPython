from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class CompanyUserDto:
    """Company user data transfer object"""
    id: str
    company_id: str
    user_id: str
    email: str | None
    role: str
    permissions: Dict[str, bool]
    status: str
    company_roles: List[str]  # IDs of assigned CompanyRole
    created_at: datetime
    updated_at: datetime
