"""
Company Page Router - Router for company page endpoints.

Company-scoped routes for managing company pages.
URL Pattern: /{company_slug}/admin/pages/*
"""
from typing import Optional, Annotated, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status as http_status

from adapters.http.company_app.company_page.controllers.company_page_controller import CompanyPageController
from adapters.http.company_app.company_page.schemas.company_page_request import CreateCompanyPageRequest, \
    UpdateCompanyPageRequest
from adapters.http.company_app.company_page.schemas.company_page_response import CompanyPageResponse, \
    CompanyPageListResponse
from adapters.http.shared.dependencies.company_context import AdminCompanyContext
from core.containers import Container

# Company-scoped router for pages
router = APIRouter(prefix="/{company_slug}/admin/pages", tags=["Company Pages"])


@router.post("", response_model=CompanyPageResponse, status_code=http_status.HTTP_201_CREATED)
@inject
async def create_company_page(
        company: AdminCompanyContext,
        request: CreateCompanyPageRequest,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Create a new company page"""
    try:
        return controller.create_page(company.id, request)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("", response_model=CompanyPageListResponse)
@inject
async def list_company_pages(
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])],
        page_type: Optional[str] = None,
        status: Optional[str] = None
) -> CompanyPageListResponse:
    """List company pages"""
    try:
        return controller.list_pages(company.id, page_type, status)
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{page_id}", response_model=CompanyPageResponse)
@inject
async def get_company_page(
        page_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Get a company page by ID"""
    try:
        return controller.get_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{page_id}", response_model=CompanyPageResponse)
@inject
async def update_company_page(
        page_id: str,
        request: UpdateCompanyPageRequest,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Update an existing company page"""
    try:
        return controller.update_page(page_id, request)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{page_id}", status_code=http_status.HTTP_204_NO_CONTENT)
@inject
async def delete_company_page(
        page_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> None:
    """Delete a company page"""
    try:
        controller.delete_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{page_id}/publish", response_model=CompanyPageResponse)
@inject
async def publish_company_page(
        page_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Publish a company page"""
    try:
        return controller.publish_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{page_id}/archive", response_model=CompanyPageResponse)
@inject
async def archive_company_page(
        page_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Archive a company page"""
    try:
        return controller.archive_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{page_id}/set-default", response_model=CompanyPageResponse)
@inject
async def set_default_company_page(
        page_id: str,
        company: AdminCompanyContext,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Set a page as default page"""
    try:
        return controller.set_default_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
