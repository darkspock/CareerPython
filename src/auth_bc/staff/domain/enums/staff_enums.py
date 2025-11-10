import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"


class StaffStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
