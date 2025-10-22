"""Delete Stage Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class DeleteStageCommand(Command):
    """Command to delete a workflow stage."""

    id: str
