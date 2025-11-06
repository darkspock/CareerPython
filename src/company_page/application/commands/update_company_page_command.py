"""
Update Company Page Command - Comando para actualizar página de empresa
"""
from dataclasses import dataclass
from typing import List, Optional

from src.shared.application.command_bus import Command


@dataclass(frozen=True)
class UpdateCompanyPageCommand(Command):
    """Comando para actualizar una página de empresa existente"""

    page_id: str
    title: str
    html_content: str
    meta_description: Optional[str]
    meta_keywords: List[str]
