"""
Archive Company Page Command - Comando para archivar página de empresa
"""
from dataclasses import dataclass

from src.shared.application.command_bus import Command


@dataclass(frozen=True)
class ArchiveCompanyPageCommand(Command):
    """Comando para archivar una página de empresa"""
    
    page_id: str
