from dataclasses import dataclass
from typing import Optional, Dict, List

from src.shared.application.command import Command


@dataclass(frozen=True)
class UpdateCompanyCandidateCommand(Command):
    """Command to update company candidate information"""
    id: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: Optional[str] = None
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    internal_notes: Optional[str] = None
