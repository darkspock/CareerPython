"""
Publish Company Page Command - Comando para publicar página de empresa
"""
from dataclasses import dataclass

from src.framework.application.command_bus import Command


@dataclass(frozen=True)
class PublishCompanyPageCommand(Command):
    """Comando para publicar una página de empresa"""
    
    page_id: str
