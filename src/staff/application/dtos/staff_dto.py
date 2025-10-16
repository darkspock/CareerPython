from typing import List

from pydantic import BaseModel

from src.staff.domain.enums.staff_enums import RoleEnum


class StaffDTO(BaseModel):
    is_staff: bool
    roles: List[RoleEnum]
