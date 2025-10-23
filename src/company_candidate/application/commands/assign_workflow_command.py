from dataclasses import dataclass
from typing import Optional

from src.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.shared.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId


@dataclass(frozen=True)
class AssignWorkflowCommand(Command):
    """Command to assign a workflow to a company candidate"""
    id: str
    workflow_id: str
    initial_stage_id: Optional[str] = None


class AssignWorkflowCommandHandler(CommandHandler[AssignWorkflowCommand]):
    """Handler for assigning a workflow to a company candidate"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def execute(self, command: AssignWorkflowCommand) -> None:
        """Handle the assign workflow command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Assign workflow
        updated_candidate = company_candidate.assign_workflow(
            workflow_id=command.workflow_id,
            initial_stage_id=command.initial_stage_id
        )

        # Save to repository
        self._repository.save(updated_candidate)