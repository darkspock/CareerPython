import io
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, Header, HTTPException
from fastapi.responses import StreamingResponse

from adapters.http.candidate_app.controllers.file_attachment_controller import FileAttachmentController
from adapters.http.candidate_app.schemas.file_attachment_response import FileAttachmentResponse
from core.containers import Container

try:
    import jwt  # type: ignore
except ImportError:
    jwt = None

router = APIRouter(prefix="/api/candidates", tags=["file-attachments"])


def get_file_attachment_controller() -> FileAttachmentController:
    """Dependency to get file attachment controller from container"""
    container = Container()
    controller: FileAttachmentController = container.candidate_container().file_attachment_controller()
    return controller


@router.post("/{candidate_id}/files", response_model=FileAttachmentResponse)
async def upload_candidate_file(
        candidate_id: str,
        file: UploadFile = File(...),
        description: str | None = Form(None),
        authorization: Optional[str] = Header(None),
        controller: FileAttachmentController = Depends(get_file_attachment_controller)
) -> FileAttachmentResponse:
    """Upload a file for a candidate"""
    # Extract company_id from JWT token
    company_id = None
    if authorization and authorization.startswith("Bearer ") and jwt:
        try:
            token = authorization.split(" ")[1]
            payload = jwt.decode(token, options={"verify_signature": False})
            company_id = payload.get("company_id")
        except Exception:
            pass

    return await controller.upload_file(candidate_id, file, description, company_id)


@router.get("/{candidate_id}/files", response_model=List[FileAttachmentResponse])
async def get_candidate_files(
        candidate_id: str,
        controller: FileAttachmentController = Depends(get_file_attachment_controller)
) -> List[FileAttachmentResponse]:
    """Get all files for a candidate"""
    return await controller.get_candidate_files(candidate_id)


@router.delete("/{candidate_id}/files/{file_id}")
async def delete_candidate_file(
        candidate_id: str,
        file_id: str,
        controller: FileAttachmentController = Depends(get_file_attachment_controller)
) -> dict:
    """Delete a file for a candidate"""
    await controller.delete_file(candidate_id, file_id)
    return {"message": "File deleted successfully"}


@router.get("/{candidate_id}/files/{file_id}/download")
async def download_file(
        candidate_id: str,
        file_id: str,
        controller: FileAttachmentController = Depends(get_file_attachment_controller)
) -> StreamingResponse:
    """Download a file"""
    # Get file info first to set proper headers
    file_response = await controller.get_file_by_id(file_id)

    # Get file content
    file_content = await controller.download_file(file_id)

    # Create a streaming response
    return StreamingResponse(
        io.BytesIO(file_content),
        media_type=file_response.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={file_response.original_name}"
        }
    )
