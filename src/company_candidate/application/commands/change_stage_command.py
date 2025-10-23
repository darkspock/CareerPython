from dataclasses import dataclass

from src.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.shared.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId


@dataclass(frozen=True)
class ChangeStageCommand(Command):
    """Command to change the workflow stage of a company candidate"""
    id: CompanyCandidateId
    new_stage_id: CompanyCandidateId


class ChangeStageCommandHandler(CommandHandler[ChangeStageCommand]):
    """Handler for changing the workflow stage of a company candidate"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def execute(self, command: ChangeStageCommand) -> None:
        """Handle the change stage command"""
        # Get existing company candidate
        company_candidate_id = command.id
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Change stage
        updated_candidate = company_candidate.change_stage(new_stage_id=command.new_stage_id)

        # Save to repository
        self._repository.save(updated_candidate)