"""
Company User router for managing users within companies.

Company-scoped routes for user management.
URL Pattern: /{company_slug}/admin/users/*
"""
import logging
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

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
from adapters.http.shared.dependencies.company_context import AdminCompanyContext, CurrentCompanyUser
from core.containers import Container
from src.company_bc.company.domain import CompanyId
from src.company_bc.company.domain.value_objects import CompanyUserId
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# Router for company user endpoints
router = APIRouter(prefix="/{company_slug}/admin/users", tags=["company-users"])


@router.post("", response_model=CompanyUserResponse, status_code=201)
@inject
async def add_company_user(
        company: AdminCompanyContext,
        request: AddCompanyUserRequest,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Add a user to a company"""
    return controller.add_company_user(company.id, request)


@router.get("", response_model=List[CompanyUserResponse])
@inject
async def list_company_users(
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
        active_only: bool = False,
) -> List[CompanyUserResponse]:
    """List all users for a company"""
    return controller.list_company_users(company.id, active_only)


@router.get("/user/{user_id}", response_model=CompanyUserResponse)
@inject
async def get_company_user_by_company_and_user(
        user_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Get a company user by company and user IDs"""
    return controller.get_company_user_by_company_and_user(company.id, user_id)


@router.get("/{company_user_id}", response_model=CompanyUserResponse)
@inject
async def get_company_user_by_id(
        company_user_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Get a company user by ID"""
    return controller.get_company_user_by_id(company_user_id)


@router.put("/{company_user_id}", response_model=CompanyUserResponse)
@inject
async def update_company_user(
        company_user_id: str,
        request: UpdateCompanyUserRequest,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Update a company user"""
    return controller.update_company_user(company_user_id, request)


@router.post("/{company_user_id}/activate", response_model=CompanyUserResponse)
@inject
async def activate_company_user(
        company_user_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Activate a company user"""
    return controller.activate_company_user(company_user_id)


@router.post("/{company_user_id}/deactivate", response_model=CompanyUserResponse)
@inject
async def deactivate_company_user(
        company_user_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Deactivate a company user"""
    return controller.deactivate_company_user(company_user_id)


@router.delete("/{user_id}", status_code=204)
@inject
async def remove_company_user(
        user_id: str,
        company: AdminCompanyContext,
        current_user: CurrentCompanyUser,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> None:
    """Remove a user from a company"""
    controller.remove_company_user(company.id, user_id, current_user.id)


@router.post("/invite", response_model=UserInvitationLinkResponse, status_code=201)
@inject
async def invite_company_user(
        company: AdminCompanyContext,
        current_user: CurrentCompanyUser,
        request: InviteCompanyUserRequest,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> UserInvitationLinkResponse:
    """Invite a user to a company"""
    return controller.invite_company_user(
        CompanyId.from_string(company.id),
        request,
        CompanyUserId.from_string(current_user.id)
    )


@router.put("/{user_id}/role", response_model=CompanyUserResponse)
@inject
async def assign_role_to_user(
        user_id: str,
        request: AssignRoleRequest,
        company: AdminCompanyContext,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> CompanyUserResponse:
    """Assign a role to a company user"""
    return controller.assign_role_to_user(company.id, user_id, request)


@router.get("/me/language", response_model=UserLanguageResponse)
@inject
async def get_company_user_language(
        company: AdminCompanyContext,
        current_user: CurrentCompanyUser,
        user_controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> UserLanguageResponse:
    """Get current company user's preferred language"""
    import traceback
    try:
        from src.company_bc.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQuery
        from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto

        # Get company user to extract user_id
        company_user_query = GetCompanyUserByIdQuery(company_user_id=current_user.id)
        company_user_dto: CompanyUserDto = query_bus.query(company_user_query)

        if not company_user_dto:
            raise HTTPException(status_code=404, detail="Company user not found")

        # Get language preference using user_id
        language_code = user_controller.get_user_language(company_user_dto.user_id)
        return UserLanguageResponse(language_code=language_code)
    except Exception as e:
        logging.error(f"Error in get_company_user_language: {e}")
        logging.error(traceback.format_exc())
        raise


@router.put("/me/language", response_model=UserLanguageUpdateResponse)
@inject
async def update_company_user_language(
        request: UserLanguageRequest,
        company: AdminCompanyContext,
        current_user: CurrentCompanyUser,
        user_controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> UserLanguageUpdateResponse:
    """Update current company user's preferred language"""
    from src.company_bc.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQuery
    from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto

    # Get company user to extract user_id
    company_user_query = GetCompanyUserByIdQuery(company_user_id=current_user.id)
    company_user_dto: CompanyUserDto = query_bus.query(company_user_query)

    if not company_user_dto:
        raise HTTPException(status_code=404, detail="Company user not found")

    # Update language preference using user_id
    result = user_controller.update_user_language(company_user_dto.user_id, request.language_code)
    return UserLanguageUpdateResponse(**result)
