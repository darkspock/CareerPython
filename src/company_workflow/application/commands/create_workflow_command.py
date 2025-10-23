from dataclasses import dataclass

from src.shared.application.command_bus import Command, CommandHandler
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.entities.company_workflow import CompanyWorkflow
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company.domain.value_objects.company_id import CompanyId


@dataclass(frozen=True)
class CreateWorkflowCommand(Command):
    """Command to create a new workflow"""
    id: str
    company_id: str
    name: str
    description: str
    is_default: bool = False


class CreateWorkflowCommandHandler(CommandHandler[CreateWorkflowCommand]):
    """Handler for creating a new workflow"""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateWorkflowCommand) -> None:
        """Handle the create workflow command"""
        workflow = CompanyWorkflow.create(
            id=CompanyWorkflowId.from_string(command.id),
            company_id=CompanyId.from_string(command.company_id),
            name=command.name,
            description=command.description,
            is_default=command.is_default
        )

        self._repository.save(workflow)