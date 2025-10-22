from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompanyWorkflowDto:
    """DTO for company workflow"""
    id: str
    company_id: str
    name: str
    description: str
    status: str
    is_default: bool
    created_at: datetime
    updated_at: datetime
