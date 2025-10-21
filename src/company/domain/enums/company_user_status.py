from enum import Enum


class CompanyUserStatus(str, Enum):
    """Company user status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
