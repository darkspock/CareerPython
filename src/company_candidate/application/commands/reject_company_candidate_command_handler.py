from src.shared.application.command import CommandHandler
from src.company_candidate.application.commands.reject_company_candidate_command import RejectCompanyCandidateCommand
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.exceptions.company_candidate_not_found import CompanyCandidateNotFound


class RejectCompanyCandidateCommandHandler(CommandHandler[RejectCompanyCandidateCommand, None]):
    """Handler for candidate rejecting company invitation"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: RejectCompanyCandidateCommand) -> None:
        """Handle the reject company candidate command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFound(f"Company candidate with id {command.id} not found")

        # Reject the invitation
        rejected_candidate = company_candidate.reject()

        # Save to repository
        self._repository.save(rejected_candidate)
