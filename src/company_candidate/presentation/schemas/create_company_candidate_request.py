from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class CreateCompanyCandidateRequest(BaseModel):
    """Request schema for creating a company candidate relationship"""
    company_id: str = Field(..., description="Company ID")

    # Either provide existing candidate_id OR candidate details to create new candidate
    candidate_id: Optional[str] = Field(None, description="Existing Candidate ID")
    candidate_name: Optional[str] = Field(None, description="Candidate name (for new candidate creation)")
    candidate_email: Optional[str] = Field(None, description="Candidate email (for new candidate creation)")
    candidate_phone: Optional[str] = Field(None, description="Candidate phone (for new candidate creation)")

    source: str = Field(default="manual_import", description="Source of the relationship")
    created_by_user_id: str = Field(..., description="Company user ID who created this relationship")
    position: Optional[str] = Field(None, description="Position/role for the candidate")
    department: Optional[str] = Field(None, description="Department")
    priority: str = Field(default="medium", description="Priority level: low, medium, high")
    visibility_settings: Optional[Dict[str, bool]] = Field(None, description="Visibility settings for candidate data")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    internal_notes: str = Field(default="", description="Internal notes about the candidate")
