from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class CreateCompanyCandidateRequest(BaseModel):
    """Request schema for creating a company candidate relationship"""
    company_id: str = Field(..., description="Company ID")
    candidate_id: str = Field(..., description="Candidate ID")
    created_by_user_id: str = Field(..., description="Company user ID who created this relationship")
    position: Optional[str] = Field(None, description="Position/role for the candidate")
    department: Optional[str] = Field(None, description="Department")
    priority: str = Field(default="medium", description="Priority level: low, medium, high")
    visibility_settings: Optional[Dict[str, bool]] = Field(None, description="Visibility settings for candidate data")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    internal_notes: str = Field(default="", description="Internal notes about the candidate")
