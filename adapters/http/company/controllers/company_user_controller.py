from typing import List, Optional
import ulid

from fastapi import HTTPException, status

from src.company.application.commands import (
    AddCompanyUserCommand,
    UpdateCompanyUserCommand,
    ActivateCompanyUserCommand,
    DeactivateCompanyUserCommand,
    RemoveCompanyUserCommand,
)
from src.company.application.queries import (
    GetCompanyUserByIdQuery,
    GetCompanyUserByCompanyAndUserQuery,
    ListCompanyUsersByCompanyQuery,
)
from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.domain import CompanyUserRole, CompanyId
from src.company.domain.exceptions.company_exceptions import (
    CompanyNotFoundError,
    CompanyValidationError,
)
from adapters.http.company.mappers.company_user_mapper import CompanyUserResponseMapper
from adapters.http.company.schemas.company_user_request import (
    AddCompanyUserRequest,
    UpdateCompanyUserRequest,
)
from adapters.http.company.schemas.company_user_response import CompanyUserResponse
from src.company.domain.value_objects import CompanyUserId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.user.domain.value_objects.UserId import UserId


class CompanyUserController:
    """Controller for CompanyUser operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def add_company_user(
        self,
        company_id: str,
        request: AddCompanyUserRequest
    ) -> CompanyUserResponse:
        """Add a user to a company"""
        try:
            # Generate new ID
            company_user_id = str(ulid.new())

            # Execute command
            command = AddCompanyUserCommand(
                id=CompanyUserId.from_string(company_user_id),
                company_id=CompanyId.from_string(company_id),
                user_id=UserId.from_string(request.user_id),
                role=CompanyUserRole(request.role),
                permissions=request.permissions,
            )
            self.command_bus.dispatch(command)

            # Query to get created company user
            query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Company user created but not found"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except CompanyValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add company user: {str(e)}"
            )

    def get_company_user_by_id(self, company_user_id: str) -> CompanyUserResponse:
        """Get a company user by ID"""
        try:
            query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company user with id {company_user_id} not found"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve company user: {str(e)}"
            )

    def get_company_user_by_company_and_user(
        self,
        company_id: str,
        user_id: str
    ) -> CompanyUserResponse:
        """Get a company user by company and user IDs"""
        try:
            query = GetCompanyUserByCompanyAndUserQuery(
                company_id=company_id,
                user_id=user_id
            )
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User {user_id} not found in company {company_id}"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve company user: {str(e)}"
            )

    def list_company_users(
        self,
        company_id: str,
        active_only: bool = False
    ) -> List[CompanyUserResponse]:
        """List all users for a company"""
        try:
            query = ListCompanyUsersByCompanyQuery(
                company_id=company_id,
                active_only=active_only
            )
            dtos: List[CompanyUserDto] = self.query_bus.query(query)

            return [CompanyUserResponseMapper.dto_to_response(dto) for dto in dtos]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list company users: {str(e)}"
            )

    def update_company_user(
        self,
        company_user_id: str,
        request: UpdateCompanyUserRequest
    ) -> CompanyUserResponse:
        """Update a company user"""
        try:
            # Execute command
            command = UpdateCompanyUserCommand(
                id=CompanyUserId.from_string(company_user_id),
                role=CompanyUserRole(request.role),
                permissions=request.permissions,
            )
            self.command_bus.dispatch(command)

            # Query to get updated company user
            query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company user with id {company_user_id} not found"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except CompanyValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update company user: {str(e)}"
            )

    def activate_company_user(self, company_user_id: str) -> CompanyUserResponse:
        """Activate a company user"""
        try:
            # Execute command
            command = ActivateCompanyUserCommand(id=CompanyUserId.from_string(company_user_id))
            self.command_bus.dispatch(command)

            # Query to get updated company user
            query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company user with id {company_user_id} not found"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to activate company user: {str(e)}"
            )

    def deactivate_company_user(self, company_user_id: str) -> CompanyUserResponse:
        """Deactivate a company user"""
        try:
            # Execute command
            command = DeactivateCompanyUserCommand(id=CompanyUserId.from_string(company_user_id))
            self.command_bus.dispatch(command)

            # Query to get updated company user
            query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
            dto: Optional[CompanyUserDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company user with id {company_user_id} not found"
                )

            return CompanyUserResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate company user: {str(e)}"
            )

    def remove_company_user(self, company_user_id: str) -> None:
        """Remove a user from a company"""
        try:
            command = RemoveCompanyUserCommand(id=company_user_id)
            self.command_bus.dispatch(command)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove company user: {str(e)}"
            )
