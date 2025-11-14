"""
Company Page Router - Router for company page endpoints
"""
from typing import Optional, Annotated, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status as http_status

from adapters.http.company_app.company_page.controllers.company_page_controller import CompanyPageController
from adapters.http.company_app.company_page.schemas.company_page_request import CreateCompanyPageRequest, \
    UpdateCompanyPageRequest
from adapters.http.company_app.company_page.schemas.company_page_response import CompanyPageResponse, \
    CompanyPageListResponse
from core.container import Container
from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_bc.company_page.application.queries.list_company_pages_query import ListCompanyPagesQuery

# Crear router
router = APIRouter(prefix="/api/company", tags=["Company Pages"])


# Private endpoints (for company management)

@router.get("/{company_id}/pages/test")
@inject
async def test_company_pages(
        company_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> dict:
    """Test endpoint to verify controller works"""
    return {"message": "Company Pages endpoint working", "company_id": company_id}


@router.get("/{company_id}/pages/test-query")
@inject
async def test_company_pages_query(
        company_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> dict:
    """Test endpoint to verify QueryBus works"""
    try:
        # Intentar usar el QueryBus directamente
        query = ListCompanyPagesQuery(company_id=company_id)
        result: List[CompanyPageDto] = controller.query_bus.query(query)
        return {"message": "QueryBus working", "result": str(result)}
    except Exception as e:
        return {"message": "QueryBus error", "error": str(e)}


@router.get("/{company_id}/pages/test-command")
@inject
async def test_company_pages_command(
        company_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> dict:
    """Test endpoint to verify CommandBus works"""
    try:
        # Intentar usar el CommandBus directamente
        from src.company_bc.company_page.application.commands.create_company_page_command import \
            CreateCompanyPageCommand
        command = CreateCompanyPageCommand(
            company_id=company_id,
            page_type="public_company_description",
            title="Test Page",
            html_content="<p>Test content</p>",
            meta_description="Test description",
            meta_keywords=["test"],
            language="es",
            is_default=False
        )
        controller.command_bus.execute(command)
        return {"message": "CommandBus working", "command": "CreateCompanyPageCommand executed"}
    except Exception as e:
        return {"message": "CommandBus error", "error": str(e)}


@router.post("/{company_id}/pages/test-create")
@inject
async def test_create_company_page(
        company_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> dict:
    """Test endpoint to verify create_page works"""
    try:
        from src.company_bc.company_page.domain.enums.page_type import PageType

        request = CreateCompanyPageRequest(
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Test Page",
            html_content="<p>Test content</p>",
            meta_description="Test description",
            meta_keywords=["test"],
            language="es",
            is_default=False
        )

        result = controller.create_page(company_id, request)
        return {"message": "Create page working", "result": str(result)}
    except Exception as e:
        return {"message": "Create page error", "error": str(e)}


@router.post("/{company_id}/pages", response_model=CompanyPageResponse, status_code=http_status.HTTP_201_CREATED)
@inject
async def create_company_page(
        company_id: str,
        request: CreateCompanyPageRequest,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Create a new company page"""
    try:
        return controller.create_page(company_id, request)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{company_id}/pages", response_model=CompanyPageListResponse)
@inject
async def list_company_pages(
        company_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])],
        page_type: Optional[str] = None,
        status: Optional[str] = None
) -> CompanyPageListResponse:
    """List company pages"""
    try:
        return controller.list_pages(company_id, page_type, status)
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/pages/{page_id}", response_model=CompanyPageResponse)
@inject
async def get_company_page(
        page_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Get a company page by ID"""
    try:
        return controller.get_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/pages/{page_id}", response_model=CompanyPageResponse)
@inject
async def update_company_page(
        page_id: str,
        request: UpdateCompanyPageRequest,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Update an existing company page"""
    try:
        return controller.update_page(page_id, request)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/pages/{page_id}", status_code=http_status.HTTP_204_NO_CONTENT)
@inject
async def delete_company_page(
        page_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> None:
    """Delete a company page"""
    try:
        controller.delete_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/publish", response_model=CompanyPageResponse)
@inject
async def publish_company_page(
        page_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Publish a company page"""
    try:
        return controller.publish_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/archive", response_model=CompanyPageResponse)
@inject
async def archive_company_page(
        page_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Archive a company page"""
    try:
        return controller.archive_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/set-default", response_model=CompanyPageResponse)
@inject
async def set_default_company_page(
        page_id: str,
        controller: Annotated[CompanyPageController, Depends(Provide[Container.company_page_controller])]
) -> CompanyPageResponse:
    """Set a page as default page"""
    try:
        return controller.set_default_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
