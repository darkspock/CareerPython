"""
Public router for company registration (no authentication required)
"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from adapters.http.company.controllers.company_controller import CompanyController
from adapters.http.company.schemas.company_registration_request import (
    CompanyRegistrationRequest,
    LinkUserRequest,
)
from adapters.http.company.schemas.company_registration_response import (
    CompanyRegistrationResponse,
    LinkUserResponse,
)
from adapters.http.shared.controllers.user import UserController
from core.container import Container
from fastapi import Query

log = logging.getLogger(__name__)

# Public router (no authentication required)
router = APIRouter(prefix="/company", tags=["company-registration"])

# Public users router for registration checks
users_router = APIRouter(prefix="/users", tags=["users-public"])


@router.post("/register", response_model=CompanyRegistrationResponse, status_code=201)
@inject
async def register_company_with_user(
        request: CompanyRegistrationRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyRegistrationResponse:
    """
    Register a new company with a new user

    This is a public endpoint (no authentication required).
    Creates:
    - New user account
    - New company
    - Links user to company as ADMIN
    - Initializes default phases and workflows
    """
    return controller.register_company_with_user(request)


@router.post("/register/link-user", response_model=LinkUserResponse, status_code=201)
@inject
async def link_user_to_company(
        request: LinkUserRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> LinkUserResponse:
    """
    Link an existing user to a new company

    This is a public endpoint (no authentication required).
    Requires:
    - Valid user email and password
    Creates:
    - New company
    - Links existing user to company as ADMIN
    - Initializes default phases and workflows
    """
    return controller.link_user_to_company(request)


@users_router.get("/check-email")
@inject
async def check_email_exists(
        user_controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        email: str = Query(..., description="Email to check"),
) -> dict:
    """
    Check if an email already exists (public endpoint for registration)

    Returns:
    - exists: Whether the email is already registered
    - can_link: Whether the user can be linked to a new company (same as exists for now)
    """
    try:
        user_exists_response = user_controller.check_user_exists(email)
        return {
            "exists": user_exists_response.exists,
            "can_link": user_exists_response.exists  # For now, if exists, can be linked
        }
    except Exception as e:
        log.error(f"Error checking email existence: {str(e)}")
        # Return default response on error
        return {"exists": False, "can_link": False}
