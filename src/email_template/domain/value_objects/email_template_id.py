"""
Email Template ID Value Object
Phase 7: Value object for email template identification
"""

import ulid
from dataclasses import dataclass


@dataclass(frozen=True)
class EmailTemplateId:
    """Value object representing an email template identifier"""

    value: str

    @staticmethod
    def generate() -> 'EmailTemplateId':
        """Generate a new unique email template ID"""
        return EmailTemplateId(str(ulid.ULID()))

    @staticmethod
    def from_string(value: str) -> 'EmailTemplateId':
        """Create EmailTemplateId from string"""
        if not value:
            raise ValueError("Email template ID cannot be empty")
        return EmailTemplateId(value)

    def __str__(self) -> str:
        return self.value
