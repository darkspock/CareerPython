"""
Create Company Page Command - Comando para crear página de empresa
"""
from dataclasses import dataclass
from typing import List, Optional

from src.framework.application.command_bus import Command


@dataclass(frozen=True)
class CreateCompanyPageCommand(Command):
    """Comando para crear una nueva página de empresa"""

    company_id: str
    page_type: str
    title: str
    html_content: str
    meta_description: Optional[str]
    meta_keywords: List[str]
    language: str
    is_default: bool
