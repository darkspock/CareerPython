from abc import ABC, abstractmethod
from typing import Optional

from core.database import DatabaseInterface
from src.shared.infrastructure.helpers.mixed_helper import MixedHelper
from src.shared.infrastructure.repositories.base import BaseRepository
from src.staff.domain.entities.staff import Staff
from src.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum
from src.staff.domain.value_objects.staff_id import StaffId
from src.staff.infrastructure.models.staff_model import StaffModel
from src.user.domain.value_objects.UserId import UserId


class StaffRepositoryInterface(ABC):
    """Interfaz para repositorio de staff"""

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> Optional[Staff]:
        pass

    @abstractmethod
    def create(self, staff: Staff) -> Staff:
        pass

    @abstractmethod
    def update_entity(self, staff: Staff) -> Staff:
        pass

    @abstractmethod
    def delete(self, id: StaffId) -> bool:
        pass


class SQLAlchemyStaffRepository(StaffRepositoryInterface):
    """Implementación de repositorio de staff con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, StaffModel)

    def _to_domain(self, model: StaffModel) -> Staff:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        return Staff(
            id=model.id,
            user_id=model.user_id,
            roles=MixedHelper.string_list_to_enum_list(model.roles, RoleEnum),
            status=StaffStatusEnum(model.status)
        )

    def _to_model(self, domain: Staff) -> StaffModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        return StaffModel(
            id=domain.id,
            user_id=domain.user_id,
            roles=MixedHelper.enum_list_to_string_list(domain.roles),
            status=domain.status
        )

    def get_by_user_id(self, user_id: UserId) -> Optional[Staff]:
        with self.database.get_session() as session:
            model = session.query(StaffModel).filter(StaffModel.user_id == user_id.value).first()
            if model:
                return self._to_domain(model)
            return None

    def create(self, staff: Staff) -> Staff:
        """Create new staff record"""
        model = self._to_model(staff)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def update_entity(self, staff: Staff) -> Staff:
        """Update staff entity directly"""
        session = self.database.get_session()
        model = session.query(StaffModel).filter(StaffModel.id == staff.id).first()
        if model:
            model.user_id = staff.user_id
            model.roles = MixedHelper.enum_list_to_string_list(staff.roles)
            model.status = staff.status
            session.commit()
            session.refresh(model)
            return self._to_domain(model)
        raise ValueError(f"Staff with id {staff.id} not found")

    def delete(self, id: StaffId) -> bool:
        """Delete staff record"""
        return self.base_repo.delete(id)
