"""Enum metadata router for company"""
from fastapi import APIRouter, Depends

from adapters.http.company_app.company.controllers.enum_controller import CompanyEnumController, CompanyEnumMetadataResponse

router = APIRouter(prefix="/api/company/enums", tags=["company-enums"])


def get_enum_controller() -> CompanyEnumController:
    """Dependency to get enum controller"""
    return CompanyEnumController()


@router.get("/metadata", response_model=CompanyEnumMetadataResponse)
async def get_enum_metadata(
    controller: CompanyEnumController = Depends(get_enum_controller)
) -> CompanyEnumMetadataResponse:
    """Get all enum definitions for company frontend consumption"""
    return controller.get_enum_metadata()
