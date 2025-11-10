import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List

from core.event import Event
from src.auth_bc.user.domain.events import (
    PasswordResetRequestedEvent
)
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass
class User:
    """Domain entity for users with subscription management"""
    id: UserId
    email: str
    hashed_password: str
    is_active: bool = True
    subscription_tier: str = 'FREE'
    subscription_expires_at: Optional[datetime] = None
    password_reset_token: Optional[str] = None
    password_reset_expires_at: Optional[datetime] = None
    preferred_language: str = 'es'  # Default to Spanish
    _domain_events: List[Event] = field(default_factory=list, init=False)

    def get_domain_events(self) -> List[Event]:
        """Get domain events raised by this entity"""
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        """Clear domain events after they have been processed"""
        self._domain_events.clear()

    def request_password_reset(self) -> str:
        """Generate password reset token and raise domain event"""
        # Generate secure random token
        reset_token = secrets.token_urlsafe(32)

        # Set token and expiry (24 hours from now)
        self.password_reset_token = reset_token
        self.password_reset_expires_at = datetime.utcnow() + timedelta(hours=24)

        # Raise domain event
        event = PasswordResetRequestedEvent(
            user_id=self.id.value,
            email=self.email,
            reset_token=reset_token,
            requested_at=datetime.utcnow(),
            expires_at=self.password_reset_expires_at
        )
        self._domain_events.append(event)

        return reset_token

    def reset_password(self, new_hashed_password: str, reset_token: str) -> bool:
        """Reset password using valid reset token"""
        # Check if token is valid and not expired
        if (self.password_reset_token != reset_token or self.password_reset_expires_at is None or
                datetime.utcnow() > self.password_reset_expires_at):
            return False

        # Update password and clear reset token
        self.hashed_password = new_hashed_password
        self.password_reset_token = None
        self.password_reset_expires_at = None

        return True

    def is_password_reset_token_valid(self, reset_token: str) -> bool:
        """Check if password reset token is valid and not expired"""
        return (self.password_reset_token == reset_token and self.password_reset_expires_at is not None
                and datetime.utcnow() <= self.password_reset_expires_at
                )

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """Generate a random password for automatic user creation"""
        import string
        import random

        # Ensure password contains at least one of each type
        password_chars = []

        # Add at least one of each required type
        password_chars.append(random.choice(string.ascii_lowercase))
        password_chars.append(random.choice(string.ascii_uppercase))
        password_chars.append(random.choice(string.digits))
        password_chars.append(random.choice("!@#$%^&*"))

        # Fill the rest with random characters
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        for _ in range(length - 4):
            password_chars.append(random.choice(all_chars))

        # Shuffle to avoid predictable patterns
        random.shuffle(password_chars)

        return ''.join(password_chars)

    def update_password(self, new_hashed_password: str) -> None:
        """Update user password (for admin operations)"""
        self.hashed_password = new_hashed_password

    def activate(self) -> None:
        """Activate user account"""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False

    def update_preferred_language(self, language_code: str) -> None:
        """Update user's preferred language"""
        # Validate language code (only allow supported languages)
        supported_languages = ['en', 'es']
        if language_code not in supported_languages:
            raise ValueError(f"Unsupported language code: {language_code}. Supported: {supported_languages}")

        self.preferred_language = language_code
