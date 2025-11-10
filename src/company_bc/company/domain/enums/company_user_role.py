from enum import Enum


class CompanyUserRole(str, Enum):
    """User roles within a company"""
    ADMIN = "admin"
    RECRUITER = "recruiter"
    VIEWER = "viewer"
