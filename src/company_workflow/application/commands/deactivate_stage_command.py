"""Deactivate Stage Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class DeactivateStageCommand(Command):
    """Command to deactivate a workflow stage."""

    id: str
