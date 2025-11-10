from typing import List

from pydantic import BaseModel

from src.auth_bc.staff.domain.enums.staff_enums import RoleEnum


class StaffDTO(BaseModel):
    is_staff: bool
    roles: List[RoleEnum]
