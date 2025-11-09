from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class UpdateCompanyCandidateRequest(BaseModel):
    """Request schema for updating company candidate information"""
    position: Optional[str] = Field(None, description="Position/role for the candidate")
    department: Optional[str] = Field(None, description="Department")
    priority: Optional[str] = Field(None, description="Priority level: low, medium, high")
    visibility_settings: Optional[Dict[str, bool]] = Field(None, description="Visibility settings for candidate data")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
