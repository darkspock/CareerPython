from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.staff.application.dtos.staff_dto import StaffDTO
from src.auth_bc.staff.infrastructure.repositories.staff_repository import SQLAlchemyStaffRepository
from src.auth_bc.user.domain.value_objects import UserId


class UserIsStaffQuery(Query):
    def __init__(self, user_id: UserId):
        self.user_id = user_id


class UserIsStaffQueryHandler(QueryHandler[UserIsStaffQuery, StaffDTO]):
    def __init__(self, staff_repository: SQLAlchemyStaffRepository):
        self.staff_repository = staff_repository

    def handle(self, query: UserIsStaffQuery) -> StaffDTO:
        staff = self.staff_repository.get_by_user_id(query.user_id)
        if staff:
            return StaffDTO(is_staff=True, roles=staff.roles)
        return StaffDTO(is_staff=False, roles=[])
