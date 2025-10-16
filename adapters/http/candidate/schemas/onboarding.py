from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class LandingRequest(BaseModel):
    """Request schema for the landing endpoint"""
    email: EmailStr
    job_position_id: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "candidate@example.com",
                "job_position_id": "01K6QZZTY8QHCVFSDXW33K2EQV"
            }
        }
    )


class LandingResponse(BaseModel):
    """Response schema for the landing endpoint"""
    success: bool
    message: str
    user_created: bool
    candidate_created: bool
    application_created: bool
    access_token: Optional[str] = None
    token_type: str = "bearer"
    analysis_job_id: Optional[str] = None  # ID of the PDF analysis job
    redirect_url: Optional[str] = None  # URL for automatic redirection

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "User created successfully. Check your email to change your password.",
                "user_created": True,
                "candidate_created": True,
                "application_created": True,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )
