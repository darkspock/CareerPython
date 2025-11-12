"""Interview Interviewer schemas"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from src.interview_bc.interview.application.queries.dtos.interview_interviewer_dto import InterviewInterviewerDto


class InviteInterviewerRequest(BaseModel):
    """Request schema for inviting an interviewer"""
    user_id: str = Field(..., description="User ID of the interviewer")
    name: Optional[str] = Field(None, description="Display name (optional)")
    is_external: bool = Field(False, description="True if interviewer is external (GUEST role)")


class AcceptInvitationRequest(BaseModel):
    """Request schema for accepting an invitation"""
    pass  # No additional fields needed, interviewer_id is in path


class InterviewInterviewerResponse(BaseModel):
    """Response schema for interview interviewer"""
    id: str = Field(..., description="Interview interviewer ID")
    interview_id: str = Field(..., description="Interview ID")
    user_id: str = Field(..., description="User ID of the interviewer")
    name: Optional[str] = Field(None, description="Display name")
    is_external: bool = Field(..., description="Whether interviewer is external")
    invited_at: Optional[datetime] = Field(None, description="When invitation was sent")
    accepted_at: Optional[datetime] = Field(None, description="When invitation was accepted")
    created_at: datetime = Field(..., description="Created datetime")
    updated_at: datetime = Field(..., description="Updated datetime")

    @classmethod
    def from_dto(cls, dto: InterviewInterviewerDto) -> "InterviewInterviewerResponse":
        """Convert DTO to response schema"""
        return cls(
            id=dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
            interview_id=dto.interview_id.value if hasattr(dto.interview_id, 'value') else str(dto.interview_id),
            user_id=dto.user_id.value if hasattr(dto.user_id, 'value') else str(dto.user_id),
            name=dto.name,
            is_external=dto.is_external,
            invited_at=dto.invited_at,
            accepted_at=dto.accepted_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    model_config = ConfigDict(from_attributes=True)


class InterviewInterviewerListResponse(BaseModel):
    """Response schema for list of interviewers"""
    interviewers: List[InterviewInterviewerResponse] = Field(..., description="List of interviewers")
    total: int = Field(..., description="Total number of interviewers")

