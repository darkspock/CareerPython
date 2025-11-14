"""
Page Type Enum - Company page types that can be created
"""
from enum import Enum


class PageType(str, Enum):
    """Available page types for companies"""

    PUBLIC_COMPANY_DESCRIPTION = "public_company_description"
    """Public company description shown on the public side"""

    JOB_POSITION_DESCRIPTION = "job_position_description"
    """Company description included in each job posting"""

    DATA_PROTECTION = "data_protection"
    """Data protection and privacy page"""

    TERMS_OF_USE = "terms_of_use"
    """Terms of use page"""

    THANK_YOU_APPLICATION = "thank_you_application"
    """Thank you page shown after applying"""
