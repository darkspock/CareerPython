from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.interview.interview.domain.enums.interview_enums import InterviewStatusEnum, InterviewTypeEnum


class InterviewProgressResponse(BaseModel):
    current_section: Optional[str]
    sections_completed: List[str]
    total_questions: int
    answered_questions: int
    completion_percentage: float
    is_paused: bool
    pause_reason: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CandidateInterviewResponse(BaseModel):
    id: str
    candidate_id: str
    status: InterviewStatusEnum
    interview_type: InterviewTypeEnum
    membership_level: Optional[str]
    interview_template_type: Optional[str]
    progress: InterviewProgressResponse
    score: Optional[float]
    feedback: Optional[str]
    created_at: Optional[datetime]
    completed_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CandidateInterviewHistoryResponse(BaseModel):
    candidate_id: str
    total_interviews: int
    completed_interviews: int
    pending_interviews: int
    cancelled_interviews: int
    average_score: Optional[float]
    latest_interview_date: Optional[datetime]
    interviews: List[CandidateInterviewResponse]
    performance_trends: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class CandidateInterviewStatsResponse(BaseModel):
    candidate_id: str
    period_days: int
    total_interviews: int
    completed_interviews: int
    pending_interviews: int
    cancelled_interviews: int
    recent_interviews_count: int
    success_rate_percentage: float
    average_score: Optional[float]
    highest_score: Optional[float]
    lowest_score: Optional[float]
    interview_types_breakdown: Dict[str, int]
    performance_trend: str  # 'improving', 'stable', 'declining', 'insufficient_data'
    recommendations: List[str]

    model_config = ConfigDict(from_attributes=True)


class InterviewListFilters(BaseModel):
    status: Optional[InterviewStatusEnum] = None
    interview_type: Optional[InterviewTypeEnum] = None
    include_answers: bool = False
    limit: Optional[int] = Field(None, ge=1, le=100)
    days_back: int = Field(365, ge=1, le=1095)  # Max 3 years
