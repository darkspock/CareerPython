"""Unset As Default Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class UnsetAsDefaultWorkflowCommand(Command):
    """Command to unset a workflow as default."""

    workflow_id: str
