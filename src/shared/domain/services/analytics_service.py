from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class ActionType(Enum):
    """Types of actions that can be tracked"""
    RESUME_DOWNLOAD = "resume_download"
    JOB_APPLICATION = "job_application"
    INTERVIEW_START = "interview_start"
    INTERVIEW_COMPLETE = "interview_complete"
    PROFILE_UPDATE = "profile_update"
    SUBSCRIPTION_UPGRADE = "subscription_upgrade"
    SUBSCRIPTION_DOWNGRADE = "subscription_downgrade"
    LOGIN = "login"
    REGISTRATION = "registration"
    PDF_UPLOAD = "pdf_upload"


@dataclass
class UsageMetrics:
    """Metrics for user usage"""
    total_users: int
    active_users_today: int
    active_users_week: int
    active_users_month: int
    total_downloads: int
    total_applications: int
    total_interviews: int


@dataclass
class SubscriptionMetrics:
    """Metrics for subscription usage"""
    free_users: int
    standard_users: int
    premium_users: int
    total_revenue: float
    conversion_rate: float
    churn_rate: float


@dataclass
class UserBehaviorMetrics:
    """Metrics for user behavior analysis"""
    avg_session_duration: float
    most_used_features: List[str]
    completion_rates: Dict[str, float]
    user_journey_stats: Dict[str, Any]


@dataclass
class SystemMetrics:
    """Overall system metrics"""
    usage_metrics: UsageMetrics
    subscription_metrics: SubscriptionMetrics
    behavior_metrics: UserBehaviorMetrics
    date_generated: datetime


class AnalyticsServiceInterface(ABC):
    """Interface for analytics service"""

    @abstractmethod
    def track_action(self, user_id: str, action_type: ActionType, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Track a user action"""
        pass

    @abstractmethod
    def get_usage_metrics(self, start_date: date, end_date: date) -> UsageMetrics:
        """Get usage metrics for a date range"""
        pass

    @abstractmethod
    def get_subscription_metrics(self, start_date: date, end_date: date) -> SubscriptionMetrics:
        """Get subscription metrics for a date range"""
        pass

    @abstractmethod
    def get_user_behavior_metrics(self, start_date: date, end_date: date) -> UserBehaviorMetrics:
        """Get user behavior metrics for a date range"""
        pass

    @abstractmethod
    def get_system_metrics(self, start_date: date, end_date: date) -> SystemMetrics:
        """Get comprehensive system metrics"""
        pass

    @abstractmethod
    def get_user_usage_summary(self, user_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Get usage summary for a specific user"""
        pass

    @abstractmethod
    def check_usage_limits(self, user_id: str, action_type: ActionType) -> Dict[str, Any]:
        """Check if user has exceeded usage limits"""
        pass
