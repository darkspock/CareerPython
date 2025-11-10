"""Invitation controller for handling invitation-related operations"""
from typing import Optional

from fastapi import HTTPException, status

from adapters.http.company.mappers.company_user_invitation_mapper import (
    CompanyUserInvitationResponseMapper
)
from adapters.http.company.schemas.company_user_invitation_request import (
    AcceptInvitationRequest
)
from adapters.http.company.schemas.company_user_invitation_response import (
    CompanyUserInvitationResponse,
)
from src.company_bc.company.application.commands.accept_user_invitation_command import (
    AcceptUserInvitationCommand
)
from src.company_bc.company.application.dtos.company_user_invitation_dto import (
    CompanyUserInvitationDto
)
from src.company_bc.company.application.queries.get_user_invitation_query import (
    GetUserInvitationQuery
)
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.auth_bc.user.domain.value_objects import UserId


class InvitationController:
    """Controller for invitation operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def get_invitation_by_token(
        self,
        token: str
    ) -> CompanyUserInvitationResponse:
        """Get invitation details by token"""
        try:
            # Convert token string to value object
            invitation_token = InvitationToken.from_string(token)
            query = GetUserInvitationQuery(token=invitation_token)
            dto: Optional[CompanyUserInvitationDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invitation not found"
                )

            return CompanyUserInvitationResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve invitation: {str(e)}"
            )

    def accept_invitation(
        self,
        request: AcceptInvitationRequest
    ) -> dict:
        """Accept a user invitation"""
        try:
            # Convert token and user_id strings to value objects
            token = InvitationToken.from_string(request.token)
            user_id = UserId.from_string(request.user_id) if request.user_id else None

            command = AcceptUserInvitationCommand(
                token=token,
                email=request.email,
                name=request.name,
                password=request.password,
                user_id=user_id
            )
            self.command_bus.dispatch(command)

            return {"message": "Invitation accepted successfully"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

