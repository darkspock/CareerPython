"""Company Role ID value object."""
from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class CompanyRoleId(BaseId):
    value: str
