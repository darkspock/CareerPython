from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class InterviewResponseFeedback(BaseModel):
    id: str
    interview_id: str
    question_id: str
    question_text: str
    response_text: str
    response_quality_score: Optional[float]
    ai_analysis: Dict[str, Any]
    keywords_extracted: List[str]
    sentiment_score: Optional[float]
    confidence_score: Optional[float]
    response_time_seconds: Optional[int]
    is_complete: bool
    follow_up_needed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InterviewFeedbackSummary(BaseModel):
    interview_id: str
    interview_type: str
    interview_status: str
    total_responses: int
    completed_responses: int
    average_quality_score: Optional[float]
    average_sentiment_score: Optional[float]
    average_confidence_score: Optional[float]
    responses_needing_followup: int
    interview_date: datetime
    feedback_highlights: List[str]
    improvement_areas: List[str]

    model_config = ConfigDict(from_attributes=True)


class CandidateFeedbackHistoryResponse(BaseModel):
    candidate_id: str
    total_interviews_with_feedback: int
    total_responses_analyzed: int
    overall_quality_score: Optional[float]
    overall_sentiment_score: Optional[float]
    overall_confidence_score: Optional[float]
    improvement_trend: str  # 'improving', 'stable', 'declining', 'insufficient_data'
    latest_feedback_date: Optional[datetime]
    interview_feedback_summaries: List[InterviewFeedbackSummary]
    performance_insights: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class CandidateFeedbackStatsResponse(BaseModel):
    candidate_id: str
    period_days: int
    total_interviews_analyzed: int
    total_responses_analyzed: int
    average_quality_score: Optional[float]
    highest_quality_score: Optional[float]
    lowest_quality_score: Optional[float]
    average_sentiment_score: Optional[float]
    average_confidence_score: Optional[float]
    common_strengths: List[str]
    areas_for_improvement: List[str]
    feedback_frequency: str  # 'high', 'medium', 'low'
    quality_trend: str  # 'improving', 'stable', 'declining'
    recommendations: List[str]

    model_config = ConfigDict(from_attributes=True)


class FeedbackFilters(BaseModel):
    interview_type: Optional[str] = None
    min_quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    follow_up_needed: Optional[bool] = None
    limit: Optional[int] = Field(None, ge=1, le=100)
    days_back: int = Field(365, ge=1, le=1095)  # Max 3 years
