from enum import Enum


class OwnershipStatus(str, Enum):
    """Ownership status of candidate data"""
    COMPANY_OWNED = "company_owned"  # Company created/owns the data
    USER_OWNED = "user_owned"  # User owns their data (read-only for company)
