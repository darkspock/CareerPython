from enum import Enum


class CompanyTypeEnum(str, Enum):
    """Company type classification
    
    Used to customize onboarding, workflows, and features based on company size and characteristics.
    """
    STARTUP_SMALL = "startup_small"
    """Startup / Small Business: 1–50 employees, fast hiring, multi-role users"""

    MID_SIZE = "mid_size"
    """Mid-Size Company: 51–500 employees, structured but flexible"""

    ENTERPRISE = "enterprise"
    """Enterprise / Large Corporation: 501+ employees, compliance-heavy, complex approvals"""

    RECRUITMENT_AGENCY = "recruitment_agency"
    """Recruitment Agency: Any size, high-volume, client-focused"""
