from dataclasses import dataclass
from typing import List

from sqlalchemy import String, Enum, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.auth_bc.staff.domain.enums.staff_enums import StaffStatusEnum
from src.framework.domain.entities.base import generate_id


@dataclass
class StaffModel(Base):
    __tablename__ = "staff"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_id)
    user_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    status: Mapped[StaffStatusEnum] = mapped_column(
        Enum(StaffStatusEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
