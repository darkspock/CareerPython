"""
Dashboard domain events for AI resume enhancement system.
Implements domain events using existing event system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List

from core.event import Event


# Profile Completion Events
@dataclass
class ProfileCompletionUpdatedEvent(Event):
    """Event fired when profile completion percentage changes."""

    user_id: str
    candidate_id: str
    previous_completion: float
    new_completion: float
    updated_sections: List[str]
    trigger_source: str  # 'dashboard_update', 'profile_edit', 'interview_complete'
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProfileSectionCompletedEvent(Event):
    """Event fired when a profile section is completed."""

    user_id: str
    candidate_id: str
    section_type: str
    completion_method: str  # 'manual', 'ai_enhanced', 'interview'
    timestamp: datetime
    section_data: Optional[Dict[str, Any]] = None


# Dashboard Activity Events
@dataclass
class DashboardViewedEvent(Event):
    """Event fired when user views dashboard."""

    user_id: str
    view_type: str  # 'overview', 'profile', 'resume', 'interview'
    session_id: Optional[str]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class QuickActionExecutedEvent(Event):
    """Event fired when user executes a quick action."""

    user_id: str
    candidate_id: str
    action_type: str  # 'add_experience', 'add_education', 'add_project'
    action_data: Dict[str, Any]
    execution_time: float  # seconds
    success: bool
    timestamp: datetime
    error_message: Optional[str] = None


# AI Enhancement Events
@dataclass
class AIRecommendationsGeneratedEvent(Event):
    """Event fired when AI recommendations are generated."""

    user_id: str
    candidate_id: str
    recommendation_count: int
    recommendation_types: List[str]
    ai_confidence_score: float
    timestamp: datetime
    recommendations: List[Dict[str, Any]]


@dataclass
class AIRecommendationAcceptedEvent(Event):
    """Event fired when user accepts an AI recommendation."""

    user_id: str
    candidate_id: str
    recommendation_id: str
    recommendation_type: str
    acceptance_method: str  # 'quick_action', 'manual_edit', 'guided_flow'
    timestamp: datetime
    outcome_data: Optional[Dict[str, Any]] = None


# Resume Events
@dataclass
class ResumePreviewGeneratedEvent(Event):
    """Event fired when resume preview is generated."""

    user_id: str
    candidate_id: str
    resume_type: str
    generation_time: float  # seconds
    ai_enhanced: bool
    timestamp: datetime
    preview_metadata: Optional[Dict[str, Any]] = None


@dataclass
class ResumeDownloadRequestedEvent(Event):
    """Event fired when user requests resume download from dashboard."""

    user_id: str
    candidate_id: str
    format_type: str
    subscription_tier: str
    remaining_downloads: Optional[int]
    timestamp: datetime
    download_metadata: Optional[Dict[str, Any]] = None


# Interview Events
@dataclass
class InterviewRestartedFromDashboardEvent(Event):
    """Event fired when interview is restarted from dashboard."""

    user_id: str
    candidate_id: str
    previous_interview_id: Optional[str]
    new_interview_id: str
    data_preserved: bool
    preserved_data_count: int
    timestamp: datetime
    restart_reason: Optional[str] = None


@dataclass
class InterviewProgressUpdatedEvent(Event):
    """Event fired when interview progress changes."""

    user_id: str
    candidate_id: str
    interview_id: str
    previous_completion: float
    new_completion: float
    section_completed: Optional[str]
    timestamp: datetime
    progress_metadata: Optional[Dict[str, Any]] = None


# Subscription Events
@dataclass
class SubscriptionLimitReachedEvent(Event):
    """Event fired when user reaches subscription limit."""

    user_id: str
    limit_type: str  # 'download', 'interview', 'ai_enhancement'
    current_tier: str
    limit_value: int
    usage_count: int
    timestamp: datetime
    blocked_action: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UpgradeRecommendationShownEvent(Event):
    """Event fired when upgrade recommendation is shown to user."""

    user_id: str
    current_tier: str
    recommended_tier: str
    trigger_action: str
    upgrade_benefits: List[str]
    timestamp: datetime
    context: str  # 'dashboard', 'download_limit', 'feature_access'


# Analytics Events
@dataclass
class DashboardMetricsCalculatedEvent(Event):
    """Event fired when dashboard metrics are calculated."""

    user_id: str
    calculation_type: str  # 'daily', 'weekly', 'session'
    metrics: Dict[str, Any]
    comparison_data: Optional[Dict[str, Any]]
    timestamp: datetime
    calculation_duration: float  # seconds


@dataclass
class UserEngagementMilestoneReachedEvent(Event):
    """Event fired when user reaches engagement milestone."""

    user_id: str
    milestone_type: str  # 'profile_complete', 'first_download', 'interview_complete'
    milestone_value: Any
    days_since_signup: int
    timestamp: datetime
    achievement_data: Optional[Dict[str, Any]] = None


# Error and Recovery Events
@dataclass
class DashboardErrorOccurredEvent(Event):
    """Event fired when dashboard error occurs."""

    user_id: Optional[str]
    error_type: str
    error_message: str
    error_context: str  # 'overview_load', 'quick_action', 'data_fetch'
    stack_trace: Optional[str]
    timestamp: datetime
    user_action: Optional[str] = None
    recovery_attempted: bool = False


@dataclass
class DashboardRecoveryAttemptedEvent(Event):
    """Event fired when dashboard recovery is attempted."""

    user_id: Optional[str]
    original_error: str
    recovery_method: str
    recovery_success: bool
    timestamp: datetime
    recovery_duration: float  # seconds
    fallback_data_used: bool = False


# Data Consistency Events
@dataclass
class DashboardDataInconsistencyDetectedEvent(Event):
    """Event fired when data inconsistency is detected."""

    user_id: str
    inconsistency_type: str
    affected_data: Dict[str, Any]
    expected_values: Dict[str, Any]
    actual_values: Dict[str, Any]
    timestamp: datetime
    auto_correction_attempted: bool = False


@dataclass
class DashboardCacheInvalidatedEvent(Event):
    """Event fired when dashboard cache is invalidated."""

    user_id: Optional[str]  # None for global cache invalidation
    cache_type: str  # 'user_overview', 'recommendations', 'metrics'
    invalidation_reason: str
    affected_components: List[str]
    timestamp: datetime
    cache_rebuild_triggered: bool = True
