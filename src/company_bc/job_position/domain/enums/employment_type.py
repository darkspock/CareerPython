import enum


class EmploymentType(str, enum.Enum):
    """Work location type enum for job positions"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    VOLUNTEER = "volunteer"
    OTHER = "other"
