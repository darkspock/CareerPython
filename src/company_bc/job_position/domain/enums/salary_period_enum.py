import enum


class SalaryPeriodEnum(str, enum.Enum):
    """Period for salary display"""
    HOURLY = "hourly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
