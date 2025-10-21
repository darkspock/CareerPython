"""
Company router for company management endpoints
"""
import logging
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Query

from core.container import Container
from src.company.presentation.controllers.company_controller import CompanyController
from src.company.presentation.schemas.company_request import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
    SuspendCompanyRequest,
)
from src.company.presentation.schemas.company_response import CompanyResponse

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
    company_id: str = Path(..., description="Company ID"),
    controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Get a company by ID"""
    return controller.get_company_by_id(company_id)


@router.get("/domain/{domain}", response_model=CompanyResponse)
@inject
async def get_company_by_domain(
    domain: str = Path(..., description="Company domain"),
    controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Get a company by domain"""
    return controller.get_company_by_domain(domain)


@router.get("", response_model=List[CompanyResponse])
@inject
async def list_companies(
    active_only: bool = Query(False, description="Filter only active companies"),
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
    company_id: str = Path(..., description="Company ID"),
    request: SuspendCompanyRequest = SuspendCompanyRequest(),
    controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Suspend a company"""
    return controller.suspend_company(company_id, request)


@router.post("/{company_id}/activate", response_model=CompanyResponse)
@inject
async def activate_company(
    company_id: str = Path(..., description="Company ID"),
    controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Activate a company"""
    return controller.activate_company(company_id)


@router.delete("/{company_id}", status_code=204)
@inject
async def delete_company(
    company_id: str = Path(..., description="Company ID"),
    controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> None:
    """Delete a company (soft delete)"""
    controller.delete_company(company_id)
