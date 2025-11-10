"""
Admin authentication middleware for validating admin roles
"""

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from adapters.http.auth.schemas.user import UserResponse
from src.framework.application.query_bus import QueryBus
from src.auth_bc.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum
from src.auth_bc.staff.infrastructure.repositories.staff_repository import SQLAlchemyStaffRepository
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery
from src.auth_bc.user.domain.value_objects import UserId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AdminAuthMiddleware:
    """Middleware to validate admin authentication and authorization"""

    def __init__(
            self,
            staff_repository: SQLAlchemyStaffRepository,
            query_bus: QueryBus
    ):
        self.staff_repository = staff_repository
        self.query_bus = query_bus

    def get_current_admin_user(self, token: str) -> UserResponse:
        """
        Get current user and validate admin role

        Args:
            token: JWT token from request

        Returns:
            UserResponse: Current authenticated admin user

        Raises:
            HTTPException: If user is not authenticated or not admin
        """
        # First validate token and get current user
        try:
            query = GetCurrentUserFromTokenQuery(token=token)
            user_dto: CurrentUserDto = self.query_bus.query(query)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is staff and has admin role
        staff = self.staff_repository.get_by_user_id(UserId.from_string(user_dto.user_id))

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin role required.",
            )

        if staff.status != StaffStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Staff account is not active.",
            )

        if RoleEnum.ADMIN not in staff.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin role required.",
            )

        return UserResponse(
            id=user_dto.user_id,
            email=user_dto.email,
            is_active=user_dto.is_active,
            is_staff=True,  # Already validated that user is staff
            roles=staff.roles  # Get roles from staff object
        )


# This function will be defined lazily to avoid circular imports
get_current_admin_user = None
