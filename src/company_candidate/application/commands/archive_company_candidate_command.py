from dataclasses import dataclass

from src.shared.application.command import Command


@dataclass(frozen=True)
class ArchiveCompanyCandidateCommand(Command):
    """Command to archive a company candidate relationship"""
    id: str
