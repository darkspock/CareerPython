from dataclasses import dataclass

from src.candidate_bc.candidate.domain.repositories.file_attachment_repository_interface import \
    FileAttachmentRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.infrastructure.storage_service_interface import StorageServiceInterface


class FileAttachmentNotFoundError(Exception):
    """Raised when file attachment is not found"""
    pass


class FileAttachmentAccessDeniedError(Exception):
    """Raised when file attachment does not belong to the specified candidate"""
    pass


@dataclass
class DeleteFileAttachmentCommand(Command):
    file_id: FileAttachmentId
    candidate_id: CandidateId


class DeleteFileAttachmentCommandHandler(CommandHandler[DeleteFileAttachmentCommand]):
    def __init__(
            self,
            file_attachment_repository: FileAttachmentRepositoryInterface,
            storage_service: StorageServiceInterface
    ):
        self.file_attachment_repository = file_attachment_repository
        self.storage_service = storage_service

    def execute(self, command: DeleteFileAttachmentCommand) -> None:
        # Get file attachment from repository
        file_attachment = self.file_attachment_repository.get_by_id(command.file_id)
        if not file_attachment:
            raise FileAttachmentNotFoundError(f"File attachment {command.file_id.value} not found")

        # Verify the file belongs to the candidate
        if file_attachment.candidate_id != command.candidate_id:
            raise FileAttachmentAccessDeniedError("File does not belong to this candidate")

        # Delete from storage
        self.storage_service.delete_file(file_attachment.file_path)

        # Delete from database
        self.file_attachment_repository.delete(command.file_id)
