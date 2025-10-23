"""
Company router for company management endpoints
"""
import logging
from typing import List, Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from adapters.http.company.controllers.company_controller import CompanyController
from adapters.http.company.schemas.company_request import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
)
from adapters.http.company.schemas.company_response import CompanyResponse
from adapters.http.shared.schemas.token import Token
from core.container import Container
from src.company.application.dtos.auth_dto import AuthenticatedCompanyUserDto
from src.company.application.queries.authenticate_company_user_query import AuthenticateCompanyUserQuery
from src.company.domain import CompanyId
from src.shared.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# Router for company endpoints
router = APIRouter(prefix="/company", tags=["company"])


@router.post("", response_model=CompanyResponse, status_code=201)
@inject
async def create_company(
        request: CreateCompanyRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Create a new company"""
    return controller.create_company(request)


@router.get("/{company_id}", response_model=CompanyResponse)
@inject
async def get_company_by_id(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Get a company by ID"""
    return controller.get_company_by_id(company_id)


@router.get("/domain/{domain}", response_model=CompanyResponse)
@inject
async def get_company_by_domain(
        domain: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Get a company by domain"""
    return controller.get_company_by_domain(domain)


@router.get("", response_model=List[CompanyResponse])
@inject
async def list_companies(
        active_only: bool,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> List[CompanyResponse]:
    """List all companies"""
    return controller.list_companies(active_only)


@router.put("/{company_id}", response_model=CompanyResponse)
@inject
async def update_company(
        company_id: str,
        request: UpdateCompanyRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Update a company"""
    return controller.update_company(company_id, request)


@router.post("/{company_id}/suspend", response_model=CompanyResponse)
@inject
async def suspend_company(
        company_id: str,
        reason: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Suspend a company"""
    return controller.suspend_company(company_id, reason)


@router.post("/{company_id}/activate", response_model=CompanyResponse)
@inject
async def activate_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Activate a company"""
    return controller.activate_company(CompanyId.from_string(company_id))


@router.delete("/{company_id}", status_code=204)
@inject
async def delete_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> None:
    """Delete a company (soft delete)"""
    controller.delete_company(company_id)


@router.post("/auth/login", response_model=Token)
@inject
async def company_login(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Authenticate company user and return JWT token"""
    try:
        # Use the authentication query to validate credentials and get token
        query = AuthenticateCompanyUserQuery(email=form_data.username, password=form_data.password)
        auth_result: Optional[AuthenticatedCompanyUserDto] = query_bus.query(query)

        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return Token(
            access_token=auth_result.access_token,
            token_type=auth_result.token_type,
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )
