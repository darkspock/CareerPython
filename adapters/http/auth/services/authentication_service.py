"""
Authentication service for handling JWT token validation across routers
"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer

from adapters.http.auth.schemas.user import UserResponse
from core.containers import Container
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# OAuth2 scheme - can be reused across different routers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="candidate/auth/login")


class AuthenticationService:
    """Service for handling authentication logic"""

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def get_current_user_from_token(self, token: str) -> UserResponse:
        """Get current user from JWT token"""
        try:
            query = GetCurrentUserFromTokenQuery(token=token)
            user_dto: CurrentUserDto = self.query_bus.query(query)
            if not user_dto:
                raise HTTPException(status_code=401, detail="Invalid token")

            return UserResponse(
                id=str(user_dto.user_id),
                email=user_dto.email,
                is_active=user_dto.is_active,
                subscription_tier="FREE"  # Default value
            )
        except Exception as e:
            log.error(f"Error getting current user: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")


# Dependency function for FastAPI
@inject
def get_current_user(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        token: str = Security(oauth2_scheme),
) -> UserResponse:
    """FastAPI dependency to get current authenticated user"""
    auth_service = AuthenticationService(query_bus)
    return auth_service.get_current_user_from_token(token)
