"""
Talent Pool Schemas
Phase 8: Request and response schemas for talent pool API
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus


# Request Schemas
class AddToTalentPoolRequest(BaseModel):
    """Request schema for adding candidate to talent pool"""

    candidate_id: str = Field(..., description="Candidate ID to add to talent pool")
    added_reason: Optional[str] = Field(None, description="Reason for adding to talent pool")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    notes: Optional[str] = Field(None, description="Additional notes")
    status: TalentPoolStatus = Field(TalentPoolStatus.ACTIVE, description="Entry status")
    source_application_id: Optional[str] = Field(None, description="Source application ID if from application")
    source_position_id: Optional[str] = Field(None, description="Source position ID if from application")


class UpdateTalentPoolEntryRequest(BaseModel):
    """Request schema for updating talent pool entry"""

    added_reason: Optional[str] = Field(None, description="Updated reason")
    tags: Optional[List[str]] = Field(None, description="Updated tags")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating from 1-5")
    notes: Optional[str] = Field(None, description="Updated notes")


class ChangeTalentPoolStatusRequest(BaseModel):
    """Request schema for changing talent pool entry status"""

    status: TalentPoolStatus = Field(..., description="New status")


# Response Schemas
class TalentPoolEntryResponse(BaseModel):
    """Response schema for talent pool entry"""

    id: str
    company_id: str
    candidate_id: str
    source_application_id: Optional[str]
    source_position_id: Optional[str]
    added_reason: Optional[str]
    tags: List[str]
    rating: Optional[int]
    notes: Optional[str]
    status: TalentPoolStatus
    added_by_user_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
