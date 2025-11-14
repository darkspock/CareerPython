"""
Company User router for managing users within companies
"""
import logging
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Security
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from adapters.http.auth.controllers.user import UserController
from adapters.http.auth.schemas.user import UserLanguageResponse, UserLanguageUpdateResponse, UserLanguageRequest
from adapters.http.company_app.company.controllers.company_user_controller import CompanyUserController
from adapters.http.company_app.company.schemas.company_user_invitation_request import (
    AssignRoleRequest,
    InviteCompanyUserRequest,
)
from adapters.http.company_app.company.schemas.company_user_invitation_response import (
    UserInvitationLinkResponse,
)
from adapters.http.company_app.company.schemas.company_user_request import (
    AddCompanyUserRequest,
    UpdateCompanyUserRequest,
)
from adapters.http.company_app.company.schemas.company_user_response import CompanyUserResponse
from core.container import Container
from src.company_bc.company.domain import CompanyId
from src.company_bc.company.domain.value_objects import CompanyUserId
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# OAuth2 scheme for company authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="company/auth/login")

# Router for company user endpoints
router = APIRouter(prefix="/company", tags=["company-users"])


def get_company_user_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_user_id from JWT token"""
    import base64
    import json
    from fastapi import HTTPException

    try:
        # Decode JWT token (payload is in the second part)
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_user_id = data.get('company_user_id') or data.get('user_id')

        if not company_user_id or not isinstance(company_user_id, str):
            raise HTTPException(status_code=401, detail="company_user_id not found in token")

        return str(company_user_id)
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/{company_id}/users", response_model=CompanyUserResponse, status_code=201)
@inject
async def add_company_user(
        company_id: str,
        request: AddCompanyUserRequest,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Add a user to a company"""
    return controller.add_company_user(company_id, request)


@router.get("/{company_id}/users", response_model=List[CompanyUserResponse])
@inject
async def list_company_users(
        company_id: str,
        active_only: bool,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> List[CompanyUserResponse]:
    """List all users for a company"""
    return controller.list_company_users(company_id, active_only)


@router.get("/{company_id}/users/user/{user_id}", response_model=CompanyUserResponse)
@inject
async def get_company_user_by_company_and_user(
        company_id: str,
        user_id: str,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Get a company user by company and user IDs"""
    return controller.get_company_user_by_company_and_user(company_id, user_id)


@router.get("/users/{company_user_id}", response_model=CompanyUserResponse)
@inject
async def get_company_user_by_id(
        company_user_id: str,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Get a company user by ID"""
    return controller.get_company_user_by_id(company_user_id)


@router.put("/users/{company_user_id}", response_model=CompanyUserResponse)
@inject
async def update_company_user(
        company_user_id: str,
        request: UpdateCompanyUserRequest,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Update a company user"""
    return controller.update_company_user(company_user_id, request)


@router.post("/users/{company_user_id}/activate", response_model=CompanyUserResponse)
@inject
async def activate_company_user(
        company_user_id: str,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Activate a company user"""
    return controller.activate_company_user(company_user_id)


@router.post("/users/{company_user_id}/deactivate", response_model=CompanyUserResponse)
@inject
async def deactivate_company_user(
        company_user_id: str,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Deactivate a company user"""
    return controller.deactivate_company_user(company_user_id)


@router.delete("/{company_id}/users/{user_id}", status_code=204)
@inject
async def remove_company_user(
        company_id: str,
        user_id: str,
        current_user_id: str,  # TODO: Get from authentication context
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> None:
    """Remove a user from a company"""
    # TODO: Get current_user_id from authenticated user context
    controller.remove_company_user(company_id, user_id, current_user_id)


@router.post("/{company_id}/users/invite", response_model=UserInvitationLinkResponse, status_code=201)
@inject
async def invite_company_user(
        company_id: str,
        request: InviteCompanyUserRequest,
        current_user_id: str,  # TODO: Get from authentication context
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> UserInvitationLinkResponse:
    """Invite a user to a company"""
    # TODO: Get current_user_id from authenticated user context
    return controller.invite_company_user(CompanyId.from_string(company_id), request,
                                          CompanyUserId.from_string(current_user_id))


@router.put("/{company_id}/users/{user_id}/role", response_model=CompanyUserResponse)
@inject
async def assign_role_to_user(
        company_id: str,
        user_id: str,
        request: AssignRoleRequest,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Assign a role to a company user"""
    return controller.assign_role_to_user(company_id, user_id, request)


@router.get("/me/language", response_model=UserLanguageResponse)
@inject
async def get_company_user_language(
        user_controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> UserLanguageResponse:
    """Get current company user's preferred language"""
    from src.company_bc.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQuery
    from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto

    # Get company user to extract user_id
    company_user_query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
    company_user_dto: CompanyUserDto = query_bus.query(company_user_query)

    if not company_user_dto:
        raise HTTPException(status_code=404, detail="Company user not found")

    # Get language preference using user_id
    language_code = user_controller.get_user_language(company_user_dto.user_id)
    return UserLanguageResponse(language_code=language_code)


@router.put("/me/language", response_model=UserLanguageUpdateResponse)
@inject
async def update_company_user_language(
        request: UserLanguageRequest,
        user_controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> UserLanguageUpdateResponse:
    """Update current company user's preferred language"""
    from src.company_bc.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQuery
    from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto

    # Get company user to extract user_id
    company_user_query = GetCompanyUserByIdQuery(company_user_id=company_user_id)
    company_user_dto: CompanyUserDto = query_bus.query(company_user_query)

    if not company_user_dto:
        raise HTTPException(status_code=404, detail="Company user not found")

    # Update language preference using user_id
    result = user_controller.update_user_language(company_user_dto.user_id, request.language_code)
    return UserLanguageUpdateResponse(**result)
