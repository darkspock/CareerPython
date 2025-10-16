import logging
from typing import Any, Optional


from presentation.candidate.schemas.candidate import CandidateResponse
from src.candidate.application.queries import GetCandidateByUserIdQuery
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.staff.application.dtos.staff_dto import StaffDTO
from src.staff.application.queries.user_is_staff_query import UserIsStaffQuery
from src.user.application.commands.create_user_command import CreateUserCommand
from src.user.application.queries.authenticate_user_query import AuthenticateUserQuery
from src.user.application.queries.create_access_token_query import CreateAccessTokenQuery
from src.user.application.queries.dtos.auth_dto import TokenDto, AuthenticatedUserDto
from src.user.domain.value_objects.UserId import UserId

log = logging.getLogger(__name__)


class AuthController:
    def __init__(
            self,
            query_bus: QueryBus,
            command_bus: CommandBus
    ):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def authenticate_user(self, email: str, password: str) -> Optional[dict[str, Any]]:
        # Use AuthenticateUserQuery instead of auth_use_case
        auth_query = AuthenticateUserQuery(email=email, password=password)
        user_dto: Optional[AuthenticatedUserDto] = self.query_bus.query(auth_query)

        if not user_dto:
            return None

        # Get staff information using query_bus
        staff_dto: StaffDTO = self.query_bus.query(UserIsStaffQuery(user_id=UserId.from_string(user_dto.user_id)))
        is_staff = staff_dto.is_staff
        roles = staff_dto.roles

        # Create access token using CreateAccessTokenQuery
        token_query = CreateAccessTokenQuery(
            data={
                "sub": user_dto.email,
                "is_staff": is_staff,
                "roles": roles
            }
        )
        token_dto: TokenDto = self.query_bus.query(token_query)

        # Get candidate information using query_bus
        candidate: Optional[CandidateResponse] = self.query_bus.query(
            GetCandidateByUserIdQuery(user_id=UserId.from_string(user_dto.user_id)))
        candidate_id = candidate.id if candidate else None

        return {
            "access_token": token_dto.access_token,
            "token_type": "bearer",
            "candidate_id": candidate_id
        }

    def create_draft_user(self, email: str, password: str) -> dict:
        """Crea un usuario en estado DRAFT"""
        log.info(f"AuthController.create_draft_user called with email: {email}")
        try:
            # Use CreateUserCommand instead of auth_use_case
            id = UserId.generate()
            create_command = CreateUserCommand(
                id=id,
                email=email,
                password=password,
                is_active=False
            )
            self.command_bus.dispatch(create_command)

            log.info(f"User created successfully: {id.value}")
            return {
                "id": id.value,
                "email": email,
                "is_active": False,
                "status": "DRAFT"
            }

        except Exception as e:
            log.error(f"Error in create_draft_user: {str(e)}")
            raise e
