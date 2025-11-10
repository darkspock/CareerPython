import enum


class WorkLocationTypeEnum(str, enum.Enum):
    """Work location type enum for job positions"""
    REMOTE = "remote"
    ON_SITE = "on_site"
    HYBRID = "hybrid"
