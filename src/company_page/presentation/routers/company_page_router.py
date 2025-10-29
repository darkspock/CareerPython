"""
Company Page Router - Router para endpoints de páginas de empresa
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.company_page.presentation.controllers.company_page_controller import CompanyPageController
from src.company_page.presentation.schemas.company_page_request import CreateCompanyPageRequest, UpdateCompanyPageRequest
from src.company_page.presentation.schemas.company_page_response import CompanyPageResponse, CompanyPageListResponse
from src.shared.presentation.dependencies import get_command_bus, get_query_bus

# Crear router
router = APIRouter(prefix="/api/company", tags=["Company Pages"])


def get_controller() -> CompanyPageController:
    """Dependency para obtener el controller"""
    command_bus = get_command_bus()
    query_bus = get_query_bus()
    return CompanyPageController(command_bus, query_bus)


# Endpoints privados (para gestión de empresa)

@router.post("/{company_id}/pages", response_model=CompanyPageResponse, status_code=status.HTTP_201_CREATED)
async def create_company_page(
    company_id: str,
    request: CreateCompanyPageRequest,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Crear una nueva página de empresa"""
    try:
        return controller.create_page(company_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{company_id}/pages", response_model=CompanyPageListResponse)
async def list_company_pages(
    company_id: str,
    status: Optional[str] = None,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageListResponse:
    """Listar páginas de una empresa"""
    try:
        return controller.list_pages(company_id, status)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/pages/{page_id}", response_model=CompanyPageResponse)
async def get_company_page(
    page_id: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Obtener una página de empresa por ID"""
    try:
        return controller.get_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/pages/{page_id}", response_model=CompanyPageResponse)
async def update_company_page(
    page_id: str,
    request: UpdateCompanyPageRequest,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Actualizar una página de empresa existente"""
    try:
        return controller.update_page(page_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/pages/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_page(
    page_id: str,
    controller: CompanyPageController = Depends(get_controller)
) -> None:
    """Eliminar una página de empresa"""
    try:
        controller.delete_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/publish", response_model=CompanyPageResponse)
async def publish_company_page(
    page_id: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Publicar una página de empresa"""
    try:
        return controller.publish_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/archive", response_model=CompanyPageResponse)
async def archive_company_page(
    page_id: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Archivar una página de empresa"""
    try:
        return controller.archive_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/pages/{page_id}/set-default", response_model=CompanyPageResponse)
async def set_default_company_page(
    page_id: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Marcar una página como página por defecto"""
    try:
        return controller.set_default_page(page_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
