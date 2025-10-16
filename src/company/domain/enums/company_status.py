import enum


class CompanyStatusEnum(str, enum.Enum):
    """Status enum for companies"""
    PENDING = "pending"
    REJECTED = "rejected"
    ACTIVE = "active"
    INACTIVE = "inactive"
