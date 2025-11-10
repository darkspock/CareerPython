from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.framework.domain.infrastructure.storage_service_interface import StorageServiceInterface, StorageType


@dataclass(frozen=True)
class UploadCandidateResumeCommand(Command):
    """Command to upload a resume for a company candidate"""
    company_candidate_id: CompanyCandidateId
    file_content: bytes
    filename: str
    content_type: str
    uploaded_by: CompanyUserId


class UploadCandidateResumeCommandHandler(CommandHandler):
    """Handler for uploading a resume for a company candidate"""

    def __init__(
        self,
        repository: CompanyCandidateRepositoryInterface,
        storage_service: StorageServiceInterface
    ):
        self._repository = repository
        self._storage_service = storage_service

    def execute(self, command: UploadCandidateResumeCommand) -> None:
        """Handle the upload resume command"""
        # Get the company candidate
        company_candidate = self._repository.get_by_id(command.company_candidate_id)
        if not company_candidate:
            raise ValueError(f"CompanyCandidate with id {command.company_candidate_id} not found")

        # Upload file to storage
        uploaded_file = self._storage_service.upload_file(
            file_content=command.file_content,
            filename=command.filename,
            content_type=command.content_type,
            storage_type=StorageType.CANDIDATE_RESUME,
            entity_id=str(company_candidate.candidate_id),
            company_id=str(company_candidate.company_id)
        )

        # Update the company candidate with the resume URL
        updated_candidate = company_candidate.update_resume(
            resume_url=uploaded_file.file_path,
            uploaded_by=command.uploaded_by
        )

        # Save to repository
        self._repository.save(updated_candidate)
