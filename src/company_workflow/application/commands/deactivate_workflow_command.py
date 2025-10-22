"""Deactivate Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class DeactivateWorkflowCommand(Command):
    """Command to deactivate a workflow."""

    workflow_id: str
