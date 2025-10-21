from dataclasses import dataclass
from datetime import datetime
from typing import Dict, bool


@dataclass
class CompanyUserDto:
    """Company user data transfer object"""
    id: str
    company_id: str
    user_id: str
    role: str
    permissions: Dict[str, bool]
    status: str
    created_at: datetime
    updated_at: datetime
