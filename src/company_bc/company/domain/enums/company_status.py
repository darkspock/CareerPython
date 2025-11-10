from enum import Enum


class CompanyStatusEnum(str, Enum):
    """Company status in the system"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"
