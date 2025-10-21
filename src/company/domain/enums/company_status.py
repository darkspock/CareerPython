from enum import Enum


class CompanyStatus(str, Enum):
    """Company status in the system"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"
