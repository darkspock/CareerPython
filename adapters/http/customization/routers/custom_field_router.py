"""Custom Field Router."""
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from core.container import Container
from src.customization.old.custom_field_controller import CustomFieldController
from src.customization.old.create_custom_field_request import CreateCustomFieldRequest
from src.customization.old.update_custom_field_request import UpdateCustomFieldRequest
from src.customization.old.reorder_custom_field_request import ReorderCustomFieldRequest
from src.customization.old.configure_stage_field_request import ConfigureStageFieldRequest
from src.customization.old.custom_field_response import CustomFieldResponse
from src.customization.old.field_configuration_response import FieldConfigurationResponse

router = APIRouter(
    prefix="/api/custom-fields",
    tags=["custom-fields"]
)


@router.post(
    "/",
    response_model=CustomFieldResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new custom field"
)
@inject
def create_custom_field(
        request: CreateCustomFieldRequest,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> CustomFieldResponse:
    """Create a new custom field for a workflow"""
    try:
        return controller.create_custom_field(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{field_id}",
    response_model=CustomFieldResponse,
    summary="Get a custom field by ID"
)
@inject
def get_custom_field_by_id(
        field_id: str,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> CustomFieldResponse:
    """Get a custom field by ID"""
    result = controller.get_custom_field_by_id(field_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Custom field not found")
    return result


@router.get(
    "/workflow/{workflow_id}",
    response_model=List[CustomFieldResponse],
    summary="List all custom fields for a workflow"
)
@inject
def list_custom_fields_by_workflow(
        workflow_id: str,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> List[CustomFieldResponse]:
    """List all custom fields for a workflow, ordered by order_index"""
    return controller.list_custom_fields_by_workflow(workflow_id)


@router.put(
    "/{field_id}",
    response_model=CustomFieldResponse,
    summary="Update a custom field"
)
@inject
def update_custom_field(
        field_id: str,
        request: UpdateCustomFieldRequest,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> CustomFieldResponse:
    """Update a custom field"""
    try:
        return controller.update_custom_field(field_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{field_id}/reorder",
    response_model=CustomFieldResponse,
    summary="Reorder a custom field"
)
@inject
def reorder_custom_field(
        field_id: str,
        request: ReorderCustomFieldRequest,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> CustomFieldResponse:
    """Change the order of a custom field"""
    try:
        return controller.reorder_custom_field(field_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{field_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a custom field"
)
@inject
def delete_custom_field(
        field_id: str,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> None:
    """Delete a custom field"""
    try:
        controller.delete_custom_field(field_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Field Configuration Endpoints

@router.post(
    "/configurations",
    response_model=FieldConfigurationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Configure field visibility for a stage"
)
@inject
def configure_stage_field(
        request: ConfigureStageFieldRequest,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> FieldConfigurationResponse:
    """Configure how a custom field behaves in a specific stage"""
    try:
        return controller.configure_stage_field(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/configurations/{config_id}/visibility",
    response_model=FieldConfigurationResponse,
    summary="Update field visibility"
)
@inject
def update_field_visibility(
        config_id: str,
        visibility: str,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> FieldConfigurationResponse:
    """Update the visibility setting for a field in a stage"""
    try:
        return controller.update_field_visibility(config_id, visibility)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/configurations/stage/{stage_id}",
    response_model=List[FieldConfigurationResponse],
    summary="List all field configurations for a stage"
)
@inject
def list_field_configurations_by_stage(
        stage_id: str,
        controller: CustomFieldController = Depends(Provide[Container.custom_field_controller])
) -> List[FieldConfigurationResponse]:
    """List all field configurations for a stage"""
    return controller.list_field_configurations_by_stage(stage_id)
