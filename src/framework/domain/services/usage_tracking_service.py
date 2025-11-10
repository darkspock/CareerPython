from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.framework.domain.services.analytics_service import ActionType


class UsageTrackingServiceInterface(ABC):
    """Interface for usage tracking service"""

    @abstractmethod
    def track_download(self, user_id: str, resume_type: str = "standard") -> None:
        """Track a resume download"""
        pass

    @abstractmethod
    def track_job_application(self, user_id: str, job_title: Optional[str] = None) -> None:
        """Track a job application creation"""
        pass

    @abstractmethod
    def track_interview_start(self, user_id: str, interview_type: str) -> None:
        """Track interview start"""
        pass

    @abstractmethod
    def track_interview_completion(self, user_id: str, interview_type: str,
                                   duration_minutes: Optional[int] = None) -> None:
        """Track interview completion"""
        pass

    @abstractmethod
    def track_profile_update(self, user_id: str, section_updated: str) -> None:
        """Track profile section update"""
        pass

    @abstractmethod
    def track_subscription_change(self, user_id: str, old_tier: str, new_tier: str) -> None:
        """Track subscription tier change"""
        pass

    @abstractmethod
    def track_user_login(self, user_id: str) -> None:
        """Track user login"""
        pass

    @abstractmethod
    def track_user_registration(self, user_id: str, registration_method: str = "email") -> None:
        """Track user registration"""
        pass

    @abstractmethod
    def track_pdf_upload(self, user_id: str, file_size_mb: Optional[float] = None) -> None:
        """Track PDF upload"""
        pass

    @abstractmethod
    def can_perform_action(self, user_id: str, action_type: ActionType) -> Dict[str, Any]:
        """Check if user can perform an action based on subscription limits"""
        pass

    @abstractmethod
    def get_user_usage_stats(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        pass
