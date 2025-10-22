"""Activate Stage Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class ActivateStageCommand(Command):
    """Command to activate a workflow stage."""

    id: str
