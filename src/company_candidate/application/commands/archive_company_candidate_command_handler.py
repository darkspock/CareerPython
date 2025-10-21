from src.shared.application.command import CommandHandler
from src.company_candidate.application.commands.archive_company_candidate_command import ArchiveCompanyCandidateCommand
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.exceptions.company_candidate_not_found import CompanyCandidateNotFound


class ArchiveCompanyCandidateCommandHandler(CommandHandler[ArchiveCompanyCandidateCommand, None]):
    """Handler for archiving a company candidate relationship"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: ArchiveCompanyCandidateCommand) -> None:
        """Handle the archive company candidate command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFound(f"Company candidate with id {command.id} not found")

        # Archive the candidate
        archived_candidate = company_candidate.archive()

        # Save to repository
        self._repository.save(archived_candidate)
