from src.shared.application.command import CommandHandler
from src.company_candidate.application.commands.change_stage_command import ChangeStageCommand
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.exceptions.company_candidate_not_found import CompanyCandidateNotFound


class ChangeStageCommandHandler(CommandHandler[ChangeStageCommand, None]):
    """Handler for changing the workflow stage of a company candidate"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: ChangeStageCommand) -> None:
        """Handle the change stage command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFound(f"Company candidate with id {command.id} not found")

        # Change stage
        updated_candidate = company_candidate.change_stage(new_stage_id=command.new_stage_id)

        # Save to repository
        self._repository.save(updated_candidate)
