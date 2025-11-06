from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from src.candidate.domain.enums import CandidateStatusEnum
from src.shared.domain.enums.job_category import JobCategoryEnum


class AdminUserResponse(BaseModel):
    """Response schema for user information in admin context"""
    id: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    # Related candidate info (if exists)
    has_candidate_profile: bool
    candidate_id: Optional[str]
    candidate_name: Optional[str]
    candidate_status: Optional[CandidateStatusEnum]
    candidate_job_category: Optional[JobCategoryEnum]
    candidate_city: Optional[str]
    candidate_country: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class AdminUserListResponse(BaseModel):
    """Response schema for paginated user list"""
    users: List[AdminUserResponse]
    total_count: int
    has_more: bool

    model_config = ConfigDict(from_attributes=True)


class UserStatsResponse(BaseModel):
    """Response schema for user statistics"""
    total_users: int
    active_users: int
    inactive_users: int
    activity_rate_percentage: float

    recent_registrations_30d: int
    recent_registrations_7d: int
    registration_growth_rate: float

    users_with_recent_login: int
    users_never_logged_in: int
    login_engagement_rate: float

    users_with_candidate_profiles: int
    users_without_candidate_profiles: int
    profile_completion_rate: float

    candidate_status_breakdown: Dict[str, int]
    geographic_distribution: List[Dict[str, Any]]
    job_category_distribution: Dict[str, int]
    monthly_registrations: List[Dict[str, Any]]

    generated_at: str

    model_config = ConfigDict(from_attributes=True)


class UserSearchFilters(BaseModel):
    """Schema for user search filters"""
    email: Optional[str] = None
    is_active: Optional[bool] = None
    has_candidate_profile: Optional[bool] = None
    created_after: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    created_before: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    last_login_after: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    last_login_before: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    search_term: Optional[str] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)
    sort_by: Optional[str] = Field("created_at", description="created_at, email, last_login")
    sort_order: Optional[str] = Field("desc", description="asc, desc")

    model_config = ConfigDict(from_attributes=True)
