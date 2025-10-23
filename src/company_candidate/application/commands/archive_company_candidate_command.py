from dataclasses import dataclass

from src.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.shared.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId


@dataclass(frozen=True)
class ArchiveCompanyCandidateCommand(Command):
    """Command to archive a company candidate relationship"""
    id: CompanyCandidateId


class ArchiveCompanyCandidateCommandHandler(CommandHandler):
    """Handler for archiving a company candidate relationship"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def execute(self, command: ArchiveCompanyCandidateCommand) -> None:
        """Handle the archive company candidate command"""
        # Get existing company candidate
        company_candidate_id = command.id
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Archive the candidate
        archived_candidate = company_candidate.archive()

        # Save to repository
        self._repository.save(archived_candidate)