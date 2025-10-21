from dataclasses import dataclass

from src.shared.application.command import Command


@dataclass(frozen=True)
class RejectCompanyCandidateCommand(Command):
    """Command for candidate to reject/decline company invitation"""
    id: str
