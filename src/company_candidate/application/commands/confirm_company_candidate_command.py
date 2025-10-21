from dataclasses import dataclass

from src.shared.application.command import Command


@dataclass(frozen=True)
class ConfirmCompanyCandidateCommand(Command):
    """Command for candidate to confirm/accept company invitation"""
    id: str
