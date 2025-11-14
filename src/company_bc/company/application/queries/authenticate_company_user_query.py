"""Authenticate Company User Query and Handler."""
from dataclasses import dataclass
from typing import Optional

from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.services.token_service import TokenService
from src.company_bc.company.application.dtos.auth_dto import AuthenticatedCompanyUserDto
from src.company_bc.company.domain.enums import CompanyUserStatus
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import \
    CompanyUserRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class AuthenticateCompanyUserQuery(Query):
    """Query to authenticate a company user with email and password."""
    email: str
    password: str


class AuthenticateCompanyUserQueryHandler(
    QueryHandler[AuthenticateCompanyUserQuery, Optional[AuthenticatedCompanyUserDto]]):
    """Handler for company user authentication query."""

    def __init__(
            self,
            user_repository: UserRepositoryInterface,
            company_user_repository: CompanyUserRepositoryInterface
    ):
        self.user_repository = user_repository
        self.company_user_repository = company_user_repository

    def handle(self, query: AuthenticateCompanyUserQuery) -> Optional[AuthenticatedCompanyUserDto]:
        """
        Handle company user authentication.

        Returns:
            AuthenticatedCompanyUserDto if authentication successful, None if failed
        """
        # Get user auth data
        user = self.user_repository.get_user_auth_data_by_email(query.email)
        if not user:
            return None

        # Verify password
        if not PasswordService.verify_password(query.password, user.hashed_password):
            return None

        # Check if user is active
        if not user.is_active:
            return None

        # Get company user relationship
        company_user = self.company_user_repository.get_by_user_id(user.id)
        if not company_user:
            return None

        # Check if company user is active
        if company_user.status != CompanyUserStatus.ACTIVE:
            return None

        # Create access token with company context
        access_token = TokenService.create_access_token(data={
            "sub": user.email,
            "user_id": user.id.value,
            "company_id": company_user.company_id.value,
            "company_user_id": company_user.id.value,
            "role": company_user.role.value
        })

        return AuthenticatedCompanyUserDto(
            user_id=user.id.value,
            company_id=company_user.company_id.value,
            email=user.email,
            role=company_user.role.value,
            access_token=access_token,
            token_type="bearer",
            is_active=user.is_active
        )
