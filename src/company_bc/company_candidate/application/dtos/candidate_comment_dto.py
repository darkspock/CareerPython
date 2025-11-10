from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CandidateCommentDto:
    """DTO for candidate comment"""
    id: str
    company_candidate_id: str
    comment: str
    workflow_id: Optional[str]
    stage_id: Optional[str]
    created_by_user_id: str
    review_status: str  # 'reviewed' or 'pending'
    visibility: str  # 'private' or 'shared_with_candidate'
    created_at: datetime
    updated_at: datetime

