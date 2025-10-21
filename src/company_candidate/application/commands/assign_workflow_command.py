from dataclasses import dataclass
from typing import Optional

from src.shared.application.command import Command


@dataclass(frozen=True)
class AssignWorkflowCommand(Command):
    """Command to assign a workflow to a company candidate"""
    id: str
    workflow_id: str
    initial_stage_id: Optional[str] = None
