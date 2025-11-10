"""
Public Company Page Router - Router for public company page endpoints
"""
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from adapters.http.company_page.controllers.company_page_controller import CompanyPageController
from src.company_page.presentation.schemas.company_page_response import CompanyPageResponse
from core.container import Container

# Crear router
router = APIRouter(prefix="/api/public/company", tags=["Public Company Pages"])


# Public endpoints (for displaying pages)

@router.get("/{company_id}/pages/{page_type}", response_model=CompanyPageResponse)
@inject
async def get_public_company_page(
    company_id: str,
    page_type: str,
    controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Get a public company page by type"""
    try:
        page = controller.get_public_page(company_id, page_type)
        
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Public page of type '{page_type}' not found for company '{company_id}'"
            )
        
        return page
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{company_id}/pages/{page_type}/default", response_model=CompanyPageResponse)
@inject
async def get_default_public_company_page(
    company_id: str,
    page_type: str,
    controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Get the default page of a specific type (alias for get_public_company_page)"""
    return await get_public_company_page(company_id, page_type, controller)
