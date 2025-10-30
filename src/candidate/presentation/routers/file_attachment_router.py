from fastapi import APIRouter, Depends, UploadFile, File, Form, Header, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional
from src.candidate.presentation.controllers.file_attachment_controller import FileAttachmentController
from src.candidate.presentation.schemas.file_attachment_response import FileAttachmentResponse
from core.container import Container
import io

router = APIRouter(prefix="/api/candidates", tags=["file-attachments"])

def get_file_attachment_controller() -> FileAttachmentController:
    """Dependency to get file attachment controller"""
    from src.candidate.infrastructure.repositories.file_attachment_repository import FileAttachmentRepository
    
    container = Container()
    storage_service = container.storage_service()
    file_repository = FileAttachmentRepository()
    return FileAttachmentController(storage_service, file_repository)

@router.post("/{candidate_id}/files", response_model=FileAttachmentResponse)
async def upload_candidate_file(
    candidate_id: str,
    file: UploadFile = File(...),
    description: str | None = Form(None),
    authorization: Optional[str] = Header(None),
    controller: FileAttachmentController = Depends(get_file_attachment_controller)
):
    """Upload a file for a candidate"""
    # Extract company_id from JWT token
    company_id = None
    if authorization and authorization.startswith("Bearer "):
        try:
            import jwt
            token = authorization.split(" ")[1]
            payload = jwt.decode(token, options={"verify_signature": False})
            company_id = payload.get("company_id")
        except:
            pass
    
    return await controller.upload_file(candidate_id, file, description, company_id)

@router.get("/{candidate_id}/files", response_model=List[FileAttachmentResponse])
async def get_candidate_files(
    candidate_id: str,
    controller: FileAttachmentController = Depends(get_file_attachment_controller)
):
    """Get all files for a candidate"""
    return await controller.get_candidate_files(candidate_id)

@router.delete("/{candidate_id}/files/{file_id}")
async def delete_candidate_file(
    candidate_id: str,
    file_id: str,
    controller: FileAttachmentController = Depends(get_file_attachment_controller)
):
    """Delete a file for a candidate"""
    await controller.delete_file(candidate_id, file_id)
    return {"message": "File deleted successfully"}

@router.get("/{candidate_id}/files/{file_id}/download")
async def download_file(
    candidate_id: str,
    file_id: str,
    controller: FileAttachmentController = Depends(get_file_attachment_controller)
):
    """Download a file"""
    # Get file info first to set proper headers
    file_attachment = controller._file_repository.get_by_id(file_id)
    if not file_attachment:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get file content
    file_content = await controller.download_file(file_id)
    
    # Create a streaming response
    file_stream = io.BytesIO(file_content)
    
    return StreamingResponse(
        io.BytesIO(file_content),
        media_type=file_attachment.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={file_attachment.original_name}"
        }
    )
