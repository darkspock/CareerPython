"""Set As Default Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command import Command


@dataclass(frozen=True)
class SetAsDefaultWorkflowCommand(Command):
    """Command to set a workflow as default for a company."""

    workflow_id: str
    company_id: str
