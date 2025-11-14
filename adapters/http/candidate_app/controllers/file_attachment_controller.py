from typing import List

from fastapi import UploadFile, HTTPException

from adapters.http.candidate_app.schemas.file_attachment_response import FileAttachmentResponse
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel
from src.candidate_bc.candidate.infrastructure.repositories.file_attachment_repository import FileAttachmentRepository
from src.framework.domain.entities.base import generate_id
from src.framework.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
    UploadedFile
)


class FileAttachmentController:
    """Controller for file attachment operations"""

    def __init__(self, storage_service: StorageServiceInterface, file_repository: FileAttachmentRepository):
        self._storage_service = storage_service
        self._file_repository = file_repository

    async def upload_file(
            self,
            candidate_id: str,
            file: UploadFile,
            description: str | None = None,
            company_id: str | None = None
    ) -> FileAttachmentResponse:
        """Upload a file for a candidate"""
        try:
            # Validate candidate exists (you might want to add this check)
            candidate_id_obj = CandidateId.from_string(candidate_id)

            # Read file content
            file_content = await file.read()

            # Upload file to storage
            uploaded_file: UploadedFile = self._storage_service.upload_file(
                file_content=file_content,
                filename=file.filename or "unknown",
                content_type=file.content_type or "application/octet-stream",
                storage_type=StorageType.INTERVIEW_ATTACHMENT,
                entity_id=candidate_id,
                company_id=company_id or "default"
            )

            # Save to database
            file_attachment = FileAttachmentModel(
                id=generate_id(),
                candidate_id=candidate_id,
                filename=uploaded_file.file_path.split('/')[-1] if uploaded_file.file_path else "unknown",
                # Extract filename from path
                original_name=file.filename or "unknown",
                file_path=uploaded_file.file_path or "",
                file_url=uploaded_file.file_url or "",
                content_type=file.content_type or "application/octet-stream",
                file_size=len(file_content),
                description=description,
                uploaded_at=uploaded_file.uploaded_at
            )

            saved_file = self._file_repository.save(file_attachment)

            # Create response
            return FileAttachmentResponse(
                id=saved_file.id,
                filename=saved_file.filename,
                original_name=saved_file.original_name,
                size=saved_file.file_size,
                content_type=saved_file.content_type,
                url=saved_file.file_url,
                file_path=saved_file.file_path,
                file_url=saved_file.file_url,
                uploaded_at=saved_file.uploaded_at,
                description=saved_file.description
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    async def get_candidate_files(self, candidate_id: str) -> List[FileAttachmentResponse]:
        """Get all files for a candidate"""
        try:
            files = self._file_repository.get_by_candidate_id(candidate_id)
            return [
                FileAttachmentResponse(
                    id=file.id,
                    filename=file.filename,
                    original_name=file.original_name,
                    size=file.file_size,
                    content_type=file.content_type,
                    url=file.file_url,
                    file_path=file.file_path,
                    file_url=file.file_url,
                    uploaded_at=file.uploaded_at,
                    description=file.description
                )
                for file in files
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get files: {str(e)}")

    async def delete_file(self, candidate_id: str, file_id: str) -> None:
        """Delete a file for a candidate"""
        try:
            # Get file from database
            file_attachment = self._file_repository.get_by_id(file_id)
            if not file_attachment:
                raise HTTPException(status_code=404, detail="File not found")

            # Verify the file belongs to the candidate
            if file_attachment.candidate_id != candidate_id:
                raise HTTPException(status_code=403, detail="File does not belong to this candidate")

            # Delete from storage
            self._storage_service.delete_file(file_attachment.file_path)

            # Delete from database
            self._file_repository.delete(file_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    async def download_file(self, file_id: str) -> bytes:
        """Download a file"""
        try:
            # Get file from database
            file_attachment = self._file_repository.get_by_id(file_id)
            if not file_attachment:
                raise HTTPException(status_code=404, detail="File not found")

            # For local storage, read the file directly
            import os
            from pathlib import Path

            # The file_path in database is relative to uploads directory
            file_path = Path("uploads") / file_attachment.file_path
            if not file_path.exists():
                raise HTTPException(status_code=404, detail=f"File not found on disk: {file_path}")

            with open(file_path, 'rb') as f:
                return f.read()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
