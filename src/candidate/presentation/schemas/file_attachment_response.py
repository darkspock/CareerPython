from datetime import datetime

from pydantic import BaseModel


class FileAttachmentResponse(BaseModel):
    """Response schema for file attachments"""
    id: str
    filename: str
    original_name: str
    size: int
    content_type: str
    url: str
    file_path: str | None = None
    file_url: str | None = None
    uploaded_at: datetime
    description: str | None = None

    class Config:
        from_attributes = True
