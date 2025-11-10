"""
Set Default Page Command - Comando para marcar página como default
"""
from dataclasses import dataclass

from src.framework.application.command_bus import Command


@dataclass(frozen=True)
class SetDefaultPageCommand(Command):
    """Comando para marcar una página como página por defecto"""
    
    page_id: str
