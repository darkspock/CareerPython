"""
Company User router for managing users within companies
"""
import logging
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from adapters.http.company.controllers.company_user_controller import CompanyUserController
from adapters.http.company.schemas.company_user_request import UpdateCompanyUserRequest, AddCompanyUserRequest
from adapters.http.company.schemas.company_user_response import CompanyUserResponse
from core.container import Container

log = logging.getLogger(__name__)

# Router for company user endpoints
router = APIRouter(prefix="/company", tags=["company-users"])


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


@router.delete("/users/{company_user_id}", status_code=204)
@inject
async def remove_company_user(
        company_user_id: str,
        controller: Annotated[CompanyUserController, Depends(Provide[Container.company_user_controller])],
) -> None:
    """Remove a user from a company"""
    controller.remove_company_user(company_user_id)
