from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

from src.shared.application.command import Command


@dataclass(frozen=True)
class CreateCompanyCandidateCommand(Command):
    """Command to create a new company candidate relationship"""
    id: str
    company_id: str
    candidate_id: str
    created_by_user_id: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: str = "medium"
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    internal_notes: str = ""
