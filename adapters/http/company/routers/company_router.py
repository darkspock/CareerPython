"""
Company router for company management endpoints
"""
import logging
from typing import List, Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
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
router = APIRouter(prefix="/companies", tags=["company"])


@router.post("", response_model=CompanyResponse, status_code=201)
@inject
async def create_company(
        request: CreateCompanyRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Create a new company"""
    return controller.create_company(request)


@router.get("/{company_id}", response_model=CompanyResponse)
@inject
async def get_company_by_id(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Get a company by ID"""
    return controller.get_company_by_id(company_id)


@router.get("/domain/{domain}", response_model=CompanyResponse)
@inject
async def get_company_by_domain(
        domain: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Get a company by domain"""
    return controller.get_company_by_domain(domain)


@router.get("/slug/{slug}", response_model=CompanyResponse)
@inject
async def get_company_by_slug(
        slug: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Get a company by slug"""
    return controller.get_company_by_slug(slug)


@router.get("", response_model=List[CompanyResponse])
@inject
async def list_companies(
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
        search_term: Optional[str] = Query(None, description="Search companies by name or domain"),
        status_filter: Optional[str] = Query(None, description="Filter by status"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
        offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> List[CompanyResponse]:
    """List all companies"""
    from src.company.domain.enums import CompanyStatusEnum

    # Convert status string to enum if provided
    status_enum = None
    if status_filter:
        try:
            status_enum = CompanyStatusEnum(status_filter.upper())
        except ValueError:
            pass

    return controller.list_companies(
        search_term=search_term,
        status_filter=status_enum,
        limit=limit,
        offset=offset
    )


@router.put("/{company_id}", response_model=CompanyResponse)
@inject
async def update_company(
        company_id: str,
        request: UpdateCompanyRequest,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Update a company"""
    return controller.update_company(company_id, request)


@router.post("/{company_id}/upload-logo", response_model=CompanyResponse)
@inject
async def upload_company_logo(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
        file: UploadFile = File(...),
) -> CompanyResponse:
    """Upload a company logo"""
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/svg+xml"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

    # Read file content
    file_content = await file.read()

    # Validate file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum allowed size of 5MB"
        )

    return controller.upload_company_logo(
        company_id=company_id,
        file_content=file_content,
        filename=file.filename or "logo.png",
        content_type=file.content_type or "image/png"
    )


@router.post("/{company_id}/suspend", response_model=CompanyResponse)
@inject
async def suspend_company(
        company_id: str,
        reason: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Suspend a company"""
    return controller.suspend_company(company_id, reason)


@router.post("/{company_id}/activate", response_model=CompanyResponse)
@inject
async def activate_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
) -> CompanyResponse:
    """Activate a company"""
    return controller.activate_company(CompanyId.from_string(company_id))


@router.delete("/{company_id}", status_code=204)
@inject
async def delete_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_management_controller])],
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
