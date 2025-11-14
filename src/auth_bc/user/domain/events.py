from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

from core.event import Event


class UserCreatedEvent(Event):
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email


@dataclass
class UserAssetCreatedEvent(Event):
    user_id: str
    asset_id: str
    asset_type: str
    content: Dict[str, Any]
    created_at: datetime

    def __init__(self, user_id: str, asset_id: str, asset_type: str, content: Dict[str, Any], created_at: datetime):
        self.user_id = user_id
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.content = content
        self.created_at = created_at


@dataclass
class UserAssetUpdatedEvent(Event):
    user_id: str
    asset_id: str
    asset_type: str
    content: Dict[str, Any]
    updated_at: datetime

    def __init__(self, user_id: str, asset_id: str, asset_type: str, content: Dict[str, Any], updated_at: datetime):
        self.user_id = user_id
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.content = content
        self.updated_at = updated_at


@dataclass
class ResumeUploadedEvent(Event):
    user_id: str
    asset_id: str
    filename: str
    extracted_text: str
    created_at: datetime
    extracted_data: Any = None  # Optional XAI extracted data

    def __init__(self, user_id: str, asset_id: str, filename: str, extracted_text: str, created_at: datetime,
                 extracted_data: Any = None):
        self.user_id = user_id
        self.asset_id = asset_id
        self.filename = filename
        self.extracted_text = extracted_text
        self.created_at = created_at
        self.extracted_data = extracted_data


@dataclass
class LinkedInProfileImportedEvent(Event):
    user_id: str
    asset_id: str
    linkedin_url: str
    profile_data: Dict[str, Any]
    created_at: datetime

    def __init__(self, user_id: str, asset_id: str, linkedin_url: str, profile_data: Dict[str, Any],
                 created_at: datetime):
        self.user_id = user_id
        self.asset_id = asset_id
        self.linkedin_url = linkedin_url
        self.profile_data = profile_data
        self.created_at = created_at


@dataclass
class SubscriptionUpgradedEvent(Event):
    """Event raised when a user's subscription is upgraded"""
    user_id: str
    previous_tier: str
    new_tier: str
    expires_at: datetime
    upgraded_at: datetime

    def __init__(self, user_id: str, previous_tier: str, new_tier: str, expires_at: datetime, upgraded_at: datetime):
        self.user_id = user_id
        self.previous_tier = previous_tier
        self.new_tier = new_tier
        self.expires_at = expires_at
        self.upgraded_at = upgraded_at


@dataclass
class SubscriptionExpiredEvent(Event):
    """Event raised when a user's subscription expires"""
    user_id: str
    expired_tier: str
    expired_at: datetime

    def __init__(self, user_id: str, expired_tier: str, expired_at: datetime):
        self.user_id = user_id
        self.expired_tier = expired_tier
        self.expired_at = expired_at


@dataclass
class SubscriptionCancelledEvent(Event):
    """Event raised when a user's subscription is cancelled"""
    user_id: str
    cancelled_tier: str
    cancelled_at: datetime
    expires_at: datetime

    def __init__(self, user_id: str, cancelled_tier: str, cancelled_at: datetime, expires_at: datetime):
        self.user_id = user_id
        self.cancelled_tier = cancelled_tier
        self.cancelled_at = cancelled_at
        self.expires_at = expires_at


@dataclass
class UsageLimitExceededEvent(Event):
    """Event raised when a user exceeds their usage limits"""
    user_id: str
    limit_type: str
    current_usage: int
    limit: int
    subscription_tier: str
    occurred_at: datetime

    def __init__(self, user_id: str, limit_type: str, current_usage: int, limit: int, subscription_tier: str,
                 occurred_at: datetime):
        self.user_id = user_id
        self.limit_type = limit_type
        self.current_usage = current_usage
        self.limit = limit
        self.subscription_tier = subscription_tier
        self.occurred_at = occurred_at


@dataclass
class ResumeDownloadedEvent(Event):
    """Event raised when a user downloads a resume"""
    user_id: str
    subscription_tier: str
    downloads_this_week: int
    download_limit: int
    downloaded_at: datetime

    def __init__(self, user_id: str, subscription_tier: str, downloads_this_week: int, download_limit: int,
                 downloaded_at: datetime):
        self.user_id = user_id
        self.subscription_tier = subscription_tier
        self.downloads_this_week = downloads_this_week
        self.download_limit = download_limit
        self.downloaded_at = downloaded_at


@dataclass
class JobApplicationCreatedEvent(Event):
    """Event raised when a user creates a job application"""
    user_id: str
    subscription_tier: str
    applications_today: int
    application_limit: int
    created_at: datetime

    def __init__(self, user_id: str, subscription_tier: str, applications_today: int, application_limit: int,
                 created_at: datetime):
        self.user_id = user_id
        self.subscription_tier = subscription_tier
        self.applications_today = applications_today
        self.application_limit = application_limit
        self.created_at = created_at


@dataclass
class PasswordResetRequestedEvent(Event):
    """Event raised when a user requests a password reset"""
    user_id: str
    email: str
    reset_token: str
    requested_at: datetime
    expires_at: datetime

    def __init__(self, user_id: str, email: str, reset_token: str, requested_at: datetime, expires_at: datetime):
        self.user_id = user_id
        self.email = email
        self.reset_token = reset_token
        self.requested_at = requested_at
        self.expires_at = expires_at


@dataclass
class UserAutoCreatedEvent(Event):
    """Event raised when a user is automatically created during PDF upload"""
    user_id: str
    email: str
    temporary_password: str
    created_at: datetime

    def __init__(self, user_id: str, email: str, temporary_password: str, created_at: datetime):
        self.user_id = user_id
        self.email = email
        self.temporary_password = temporary_password
        self.created_at = created_at
