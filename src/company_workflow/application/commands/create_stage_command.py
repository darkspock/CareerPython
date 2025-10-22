"""Create Stage Command."""
from dataclasses import dataclass
from typing import Optional
from src.shared.application.command import Command


@dataclass(frozen=True)
class CreateStageCommand(Command):
    """Command to create a new workflow stage."""

    id: str
    workflow_id: str
    name: str
    description: str
    stage_type: str
    order: int
    required_outcome: Optional[str] = None
    estimated_duration_days: Optional[int] = None
    is_active: bool = True
