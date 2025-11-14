"""
Invitation router for public invitation endpoints
"""
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from adapters.http.auth.invitations.controllers.invitation_controller import (
    InvitationController
)
from adapters.http.company_app.company.schemas.company_user_invitation_request import (
    AcceptInvitationRequest
)
from adapters.http.company_app.company.schemas.company_user_invitation_response import (
    CompanyUserInvitationResponse,
)
from core.container import Container

# Router for invitation endpoints (public, no authentication required)
router = APIRouter(prefix="/invitations", tags=["invitations"])


@router.get("/{token}", response_model=CompanyUserInvitationResponse)
@inject
async def get_invitation_by_token(
        token: str,
        controller: Annotated[
            InvitationController,
            Depends(Provide[Container.invitation_controller])
        ],
) -> CompanyUserInvitationResponse:
    """Get invitation details by token (public endpoint)"""
    return controller.get_invitation_by_token(token)


@router.post("/accept", status_code=200)
@inject
async def accept_invitation(
        request: AcceptInvitationRequest,
        controller: Annotated[
            InvitationController,
            Depends(Provide[Container.invitation_controller])
        ],
) -> dict:
    """Accept a user invitation (public endpoint)"""
    return controller.accept_invitation(request)
