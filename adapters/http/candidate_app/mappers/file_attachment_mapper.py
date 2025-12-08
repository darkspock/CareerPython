"""File Attachment Mapper - Converts DTOs to Response schemas"""
from __future__ import annotations
from typing import List, TYPE_CHECKING

from src.candidate_bc.candidate.application.queries.shared.file_attachment_dto import FileAttachmentDto

if TYPE_CHECKING:
    from adapters.http.candidate_app.schemas.file_attachment_response import FileAttachmentResponse


class FileAttachmentMapper:
    """Mapper for converting file attachment DTOs to response schemas"""

    @classmethod
    def dto_to_response(cls, dto: FileAttachmentDto) -> "FileAttachmentResponse":
        """Convert FileAttachmentDto to FileAttachmentResponse"""
        from adapters.http.candidate_app.schemas.file_attachment_response import FileAttachmentResponse

        return FileAttachmentResponse(
            id=dto.id.value,
            filename=dto.filename,
            original_name=dto.original_name,
            size=dto.file_size,
            content_type=dto.content_type,
            url=dto.file_url,
            file_path=dto.file_path,
            file_url=dto.file_url,
            uploaded_at=dto.uploaded_at,
            description=dto.description
        )

    @classmethod
    def dtos_to_responses(cls, dtos: List[FileAttachmentDto]) -> List["FileAttachmentResponse"]:
        """Convert list of FileAttachmentDto to list of FileAttachmentResponse"""
        return [cls.dto_to_response(dto) for dto in dtos]
