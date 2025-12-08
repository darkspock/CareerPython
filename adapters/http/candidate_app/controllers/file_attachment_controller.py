from pathlib import Path
from typing import List, Optional

from fastapi import UploadFile, HTTPException

from adapters.http.candidate_app.mappers.file_attachment_mapper import FileAttachmentMapper
from adapters.http.candidate_app.schemas.file_attachment_response import FileAttachmentResponse
from src.candidate_bc.candidate.application.commands.delete_file_attachment import (
    DeleteFileAttachmentCommand,
    FileAttachmentNotFoundError,
    FileAttachmentAccessDeniedError
)
from src.candidate_bc.candidate.application.commands.upload_file_attachment import UploadFileAttachmentCommand
from src.candidate_bc.candidate.application.queries.get_file_attachment_by_id import GetFileAttachmentByIdQuery
from src.candidate_bc.candidate.application.queries.list_file_attachments_by_candidate import \
    ListFileAttachmentsByCandidateQuery
from src.candidate_bc.candidate.application.queries.shared.file_attachment_dto import FileAttachmentDto
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.framework.domain.entities.base import generate_id


class FileAttachmentController:
    """Controller for file attachment operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    async def upload_file(
            self,
            candidate_id: str,
            file: UploadFile,
            description: str | None = None,
            company_id: str | None = None
    ) -> FileAttachmentResponse:
        """Upload a file for a candidate"""
        try:
            # Validate candidate_id
            candidate_id_vo = CandidateId.from_string(candidate_id)

            # Read file content
            file_content = await file.read()

            # Create command with a new ID
            file_attachment_id = FileAttachmentId.from_string(generate_id())
            command = UploadFileAttachmentCommand(
                id=file_attachment_id,
                candidate_id=candidate_id_vo,
                file_content=file_content,
                filename=file.filename or "unknown",
                content_type=file.content_type or "application/octet-stream",
                description=description,
                company_id=company_id
            )

            # Execute command
            self._command_bus.dispatch(command)

            # Query to get the created file attachment
            query = GetFileAttachmentByIdQuery(file_id=file_attachment_id)
            dto: Optional[FileAttachmentDto] = self._query_bus.query(query)

            if not dto:
                raise HTTPException(status_code=500, detail="Failed to retrieve uploaded file")

            return FileAttachmentMapper.dto_to_response(dto)

        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    async def get_candidate_files(self, candidate_id: str) -> List[FileAttachmentResponse]:
        """Get all files for a candidate"""
        try:
            candidate_id_vo = CandidateId.from_string(candidate_id)
            query = ListFileAttachmentsByCandidateQuery(candidate_id=candidate_id_vo)
            dtos: List[FileAttachmentDto] = self._query_bus.query(query)
            return FileAttachmentMapper.dtos_to_responses(dtos)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get files: {str(e)}")

    async def delete_file(self, candidate_id: str, file_id: str) -> None:
        """Delete a file for a candidate"""
        try:
            candidate_id_vo = CandidateId.from_string(candidate_id)
            file_id_vo = FileAttachmentId.from_string(file_id)

            command = DeleteFileAttachmentCommand(
                file_id=file_id_vo,
                candidate_id=candidate_id_vo
            )
            self._command_bus.dispatch(command)

        except FileAttachmentNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except FileAttachmentAccessDeniedError:
            raise HTTPException(status_code=403, detail="File does not belong to this candidate")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    async def get_file_by_id(self, file_id: str) -> FileAttachmentResponse:
        """Get a file by ID"""
        file_id_vo = FileAttachmentId.from_string(file_id)
        query = GetFileAttachmentByIdQuery(file_id=file_id_vo)
        dto: Optional[FileAttachmentDto] = self._query_bus.query(query)

        if not dto:
            raise HTTPException(status_code=404, detail="File not found")

        return FileAttachmentMapper.dto_to_response(dto)

    async def download_file(self, file_id: str) -> bytes:
        """Download a file"""
        try:
            file_id_vo = FileAttachmentId.from_string(file_id)
            query = GetFileAttachmentByIdQuery(file_id=file_id_vo)
            dto: Optional[FileAttachmentDto] = self._query_bus.query(query)

            if not dto:
                raise HTTPException(status_code=404, detail="File not found")

            # For local storage, read the file directly
            file_path = Path("uploads") / dto.file_path
            if not file_path.exists():
                raise HTTPException(status_code=404, detail=f"File not found on disk: {file_path}")

            with open(file_path, 'rb') as f:
                return f.read()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
