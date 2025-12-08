from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate_bc.candidate.domain.entities.file_attachment import FileAttachment
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class FileAttachmentDto:
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
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: FileAttachment) -> 'FileAttachmentDto':
        return cls(
            id=entity.id,
            candidate_id=entity.candidate_id,
            filename=entity.filename,
            original_name=entity.original_name,
            file_path=entity.file_path,
            file_url=entity.file_url,
            content_type=entity.content_type,
            file_size=entity.file_size,
            description=entity.description,
            uploaded_at=entity.uploaded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
