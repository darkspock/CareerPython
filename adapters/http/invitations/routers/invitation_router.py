"""
Invitation router for public invitation endpoints
"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from adapters.http.company.schemas.company_user_invitation_request import AcceptInvitationRequest
from adapters.http.company.schemas.company_user_invitation_response import (
    CompanyUserInvitationResponse,
)
from adapters.http.company.controllers.company_user_controller import CompanyUserController
from src.company.application.queries.get_user_invitation_query import GetUserInvitationQuery
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from core.container import Container

log = logging.getLogger(__name__)

# Router for invitation endpoints (public, no authentication required)
router = APIRouter(prefix="/invitations", tags=["invitations"])


@router.get("/{token}", response_model=CompanyUserInvitationResponse)
@inject
async def get_invitation_by_token(
        token: str,
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> CompanyUserInvitationResponse:
    """Get invitation details by token (public endpoint)"""
    from adapters.http.company.mappers.company_user_invitation_mapper import (
        CompanyUserInvitationResponseMapper
    )
    
    from src.company.domain.value_objects.invitation_token import InvitationToken
    
    try:
        # Convert token string to value object
        invitation_token = InvitationToken.from_string(token)
        query = GetUserInvitationQuery(token=invitation_token)
        dto = query_bus.query(query)

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


@router.post("/accept", status_code=200)
@inject
async def accept_invitation(
        request: AcceptInvitationRequest,
        command_bus: Annotated[CommandBus, Depends(Provide[Container.command_bus])],
) -> dict:
    """Accept a user invitation (public endpoint)"""
    from src.company.application.commands.accept_user_invitation_command import (
        AcceptUserInvitationCommand
    )
    
    from src.company.domain.value_objects.invitation_token import InvitationToken
    from src.user.domain.value_objects.UserId import UserId
    
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
        command_bus.dispatch(command)

        return {"message": "Invitation accepted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

