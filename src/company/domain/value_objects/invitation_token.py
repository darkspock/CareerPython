import secrets
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InvitationToken:
    """Invitation token for company user invitations"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("InvitationToken cannot be empty")
        if len(self.value) < 16:
            raise ValueError("InvitationToken must be at least 16 characters")

    @classmethod
    def generate(cls) -> "InvitationToken":
        """Generate a new secure invitation token"""
        return cls(secrets.token_urlsafe(32))

    @classmethod
    def from_string(cls, token_str: str) -> "InvitationToken":
        """Create InvitationToken from string"""
        if not token_str:
            raise ValueError("Token string cannot be empty")
        return cls(token_str)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InvitationToken):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

