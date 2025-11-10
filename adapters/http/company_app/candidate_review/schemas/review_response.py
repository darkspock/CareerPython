from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewResponse(BaseModel):
    """Candidate review API response schema"""
    id: str
    company_candidate_id: str
    score: int  # 0, 3, 6, 10
    comment: Optional[str]
    workflow_id: Optional[str]
    stage_id: Optional[str]
    review_status: str  # 'pending' or 'reviewed'
    created_by_user_id: str
    created_at: datetime
    updated_at: datetime
    # Expanded data (optional, may be populated by API)
    workflow_name: Optional[str] = None
    stage_name: Optional[str] = None
    created_by_user_name: Optional[str] = None
    created_by_user_email: Optional[str] = None

    class Config:
        from_attributes = True

