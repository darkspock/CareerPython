from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.domain.entities.file_attachment import FileAttachment
from src.candidate_bc.candidate.domain.repositories.file_attachment_repository_interface import \
    FileAttachmentRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType
)


@dataclass
class UploadFileAttachmentCommand(Command):
    id: FileAttachmentId
    candidate_id: CandidateId
    file_content: bytes
    filename: str
    content_type: str
    description: Optional[str]
    company_id: Optional[str]


class UploadFileAttachmentCommandHandler(CommandHandler[UploadFileAttachmentCommand]):
    def __init__(
            self,
            file_attachment_repository: FileAttachmentRepositoryInterface,
            storage_service: StorageServiceInterface
    ):
        self.file_attachment_repository = file_attachment_repository
        self.storage_service = storage_service

    def execute(self, command: UploadFileAttachmentCommand) -> None:
        # Upload file to storage
        uploaded_file = self.storage_service.upload_file(
            file_content=command.file_content,
            filename=command.filename,
            content_type=command.content_type,
            storage_type=StorageType.INTERVIEW_ATTACHMENT,
            entity_id=command.candidate_id.value,
            company_id=command.company_id or "default"
        )

        # Create domain entity
        file_attachment = FileAttachment.create(
            id=command.id,
            candidate_id=command.candidate_id,
            filename=uploaded_file.file_path.split('/')[-1] if uploaded_file.file_path else "unknown",
            original_name=command.filename,
            file_path=uploaded_file.file_path or "",
            file_url=uploaded_file.file_url or "",
            content_type=command.content_type,
            file_size=len(command.file_content),
            uploaded_at=uploaded_file.uploaded_at,
            description=command.description
        )

        # Save to database
        self.file_attachment_repository.save(file_attachment)
