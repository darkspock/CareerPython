"""
Public Company Page Router - Router para endpoints públicos de páginas de empresa
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.company_page.presentation.controllers.company_page_controller import CompanyPageController
from src.company_page.presentation.schemas.company_page_response import CompanyPageResponse
from src.shared.presentation.dependencies import get_command_bus, get_query_bus

# Crear router
router = APIRouter(prefix="/api/public/company", tags=["Public Company Pages"])


def get_controller() -> CompanyPageController:
    """Dependency para obtener el controller"""
    command_bus = get_command_bus()
    query_bus = get_query_bus()
    return CompanyPageController(command_bus, query_bus)


# Endpoints públicos (para mostrar páginas)

@router.get("/{company_id}/pages/{page_type}", response_model=CompanyPageResponse)
async def get_public_company_page(
    company_id: str,
    page_type: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Obtener una página pública de empresa por tipo"""
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
async def get_default_public_company_page(
    company_id: str,
    page_type: str,
    controller: CompanyPageController = Depends(get_controller)
) -> CompanyPageResponse:
    """Obtener la página por defecto de un tipo específico (alias para get_public_company_page)"""
    return await get_public_company_page(company_id, page_type, controller)
