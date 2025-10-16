from dataclasses import dataclass, field
from typing import List

from src.shared.domain.entities.base import generate_id
from src.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum


@dataclass
class Staff:
    user_id: str
    roles: List[RoleEnum]
    status: StaffStatusEnum
    id: str = field(default_factory=generate_id)
