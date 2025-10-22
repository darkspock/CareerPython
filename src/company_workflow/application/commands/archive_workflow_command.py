"""Archive Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class ArchiveWorkflowCommand(Command):
    """Command to archive a workflow."""

    workflow_id: str
