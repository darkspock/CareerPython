from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CandidateCommentResponse(BaseModel):
    """Candidate comment API response schema"""
    id: str
    company_candidate_id: str
    comment: str
    workflow_id: Optional[str]
    stage_id: Optional[str]
    created_by_user_id: str
    review_status: str
    visibility: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

