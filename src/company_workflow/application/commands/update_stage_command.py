"""Update Stage Command."""
from dataclasses import dataclass
from typing import Optional
from src.shared.application.command import Command


@dataclass(frozen=True)
class UpdateStageCommand(Command):
    """Command to update a workflow stage."""

    id: str
    name: str
    description: str
    required_outcome: Optional[str] = None
    estimated_duration_days: Optional[int] = None
