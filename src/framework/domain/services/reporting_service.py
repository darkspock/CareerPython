from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Any, Optional


@dataclass
class DashboardMetrics:
    """Metrics for the admin dashboard"""
    total_users: int
    active_users_today: int
    active_users_week: int
    new_registrations_today: int
    new_registrations_week: int
    total_downloads: int
    total_applications: int
    revenue_today: float
    revenue_week: float
    revenue_month: float
    top_features: List[Dict[str, Any]]
    subscription_distribution: Dict[str, int]
    user_growth_trend: List[Dict[str, Any]]


@dataclass
class UserDashboardMetrics:
    """Metrics for user's personal dashboard"""
    user_id: str
    subscription_tier: str
    downloads_used: int
    downloads_remaining: int
    applications_used: int
    applications_remaining: int
    profile_completion: float
    last_activity: str
    recent_activities: List[Dict[str, Any]]
    usage_trends: Dict[str, List[int]]


class ReportingServiceInterface(ABC):
    """Interface for reporting service"""

    @abstractmethod
    def get_admin_dashboard_metrics(self, date_range: Optional[int] = 30) -> DashboardMetrics:
        """Get metrics for admin dashboard"""
        pass

    @abstractmethod
    def get_user_dashboard_metrics(self, user_id: str) -> UserDashboardMetrics:
        """Get metrics for user's personal dashboard"""
        pass

    @abstractmethod
    def generate_usage_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate comprehensive usage report"""
        pass

    @abstractmethod
    def generate_subscription_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate subscription analytics report"""
        pass

    @abstractmethod
    def generate_feature_usage_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate feature usage analytics report"""
        pass

    @abstractmethod
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time system metrics"""
        pass
