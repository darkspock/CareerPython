from enum import Enum


class RegistrationStatusEnum(str, Enum):
    """Status of user registration"""
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"


class ProcessingStatusEnum(str, Enum):
    """Processing status of PDF extraction"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
