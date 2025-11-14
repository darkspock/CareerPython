"""Phase status enumeration"""
from enum import Enum


class PhaseStatus(str, Enum):
    """Status of a recruitment phase"""
    DRAFT = "DRAFT"  # Phase is being configured, not yet active
    ACTIVE = "ACTIVE"  # Phase is active and in use
    ARCHIVED = "ARCHIVED"  # Phase has been archived (soft delete)
