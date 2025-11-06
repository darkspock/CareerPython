"""
Delete Company Page Command - Comando para eliminar página de empresa
"""
from dataclasses import dataclass

from src.shared.application.command_bus import Command


@dataclass(frozen=True)
class DeleteCompanyPageCommand(Command):
    """Comando para eliminar una página de empresa"""

    page_id: str
