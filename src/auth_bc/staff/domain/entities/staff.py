from dataclasses import dataclass, field
from typing import List

from src.auth_bc.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum
from src.framework.domain.entities.base import generate_id


@dataclass
class Staff:
    user_id: str
    roles: List[RoleEnum]
    status: StaffStatusEnum
    id: str = field(default_factory=generate_id)
