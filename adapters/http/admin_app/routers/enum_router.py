"""Enum metadata router"""
from fastapi import APIRouter, Depends

from adapters.http.admin_app.controllers.enum_controller import EnumController, EnumMetadataResponse

router = APIRouter(prefix="/admin/enums", tags=["admin-enums"])


def get_enum_controller() -> EnumController:
    """Dependency to get enum controller"""
    return EnumController()


@router.get("/metadata", response_model=EnumMetadataResponse)
async def get_enum_metadata(
    controller: EnumController = Depends(get_enum_controller)
) -> EnumMetadataResponse:
    """Get all enum definitions for frontend consumption"""
    return controller.get_enum_metadata()
