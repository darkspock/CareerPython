from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class FileAttachment:
    """Domain entity for file attachments"""
    id: FileAttachmentId
    candidate_id: CandidateId
    filename: str
    original_name: str
    file_path: str
    file_url: str
    content_type: str
    file_size: int
    description: Optional[str]
    uploaded_at: datetime
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(
            id: FileAttachmentId,
            candidate_id: CandidateId,
            filename: str,
            original_name: str,
            file_path: str,
            file_url: str,
            content_type: str,
            file_size: int,
            uploaded_at: datetime,
            description: Optional[str] = None
    ) -> 'FileAttachment':
        """Factory method to create a new FileAttachment"""
        return FileAttachment(
            id=id,
            candidate_id=candidate_id,
            filename=filename,
            original_name=original_name,
            file_path=file_path,
            file_url=file_url,
            content_type=content_type,
            file_size=file_size,
            description=description,
            uploaded_at=uploaded_at
        )

    def update_description(self, description: Optional[str]) -> None:
        """Update the file description"""
        self.description = description
        self.updated_at = datetime.now()
