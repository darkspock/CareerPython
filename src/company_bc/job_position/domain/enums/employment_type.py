import enum


class EmploymentTypeEnum(str, enum.Enum):
    """Employment type enum for job positions"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    VOLUNTEER = "volunteer"
    OTHER = "other"


# Alias for backwards compatibility
EmploymentType = EmploymentTypeEnum
