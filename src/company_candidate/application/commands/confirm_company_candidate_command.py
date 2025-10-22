from dataclasses import dataclass

from src.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.shared.application.command import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId


@dataclass(frozen=True)
class ConfirmCompanyCandidateCommand(Command):
    """Command for candidate to confirm/accept company invitation"""
    id: str


class ConfirmCompanyCandidateCommandHandler(CommandHandler[ConfirmCompanyCandidateCommand, None]):
    """Handler for candidate confirming company invitation"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: ConfirmCompanyCandidateCommand) -> None:
        """Handle the confirm company candidate command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Confirm the invitation
        confirmed_candidate = company_candidate.confirm()

        # Save to repository
        self._repository.save(confirmed_candidate)