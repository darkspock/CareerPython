"""Custom Field Value Router."""
from typing import Dict, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from core.container import Container
from src.customization.custom_field_value_controller import CustomFieldValueController
from src.workflow.presentation.schemas.create_custom_field_value_request import CreateCustomFieldValueRequest
from src.workflow.presentation.schemas.update_custom_field_value_request import UpdateCustomFieldValueRequest
from src.workflow.presentation.schemas.custom_field_value_response import CustomFieldValueResponse

router = APIRouter(prefix="/custom-field-values", tags=["Custom Field Values"])


@router.post("", response_model=CustomFieldValueResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_custom_field_value(
    request: CreateCustomFieldValueRequest,
    controller: CustomFieldValueController = Depends(Provide[Container.custom_field_value_controller])
) -> CustomFieldValueResponse:
    """Create a new custom field value"""
    try:
        return controller.create_custom_field_value(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{value_id}", response_model=CustomFieldValueResponse)
@inject
def get_custom_field_value(
    value_id: str,
    controller: CustomFieldValueController = Depends(Provide[Container.custom_field_value_controller])
) -> CustomFieldValueResponse:
    """Get a custom field value by ID"""
    result = controller.get_custom_field_value_by_id(value_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Custom field value not found"
        )
    return result


@router.get("/company-candidate/{company_candidate_id}", response_model=Dict[str, Any])
@inject
def get_custom_field_values_by_company_candidate(
    company_candidate_id: str,
    controller: CustomFieldValueController = Depends(Provide[Container.custom_field_value_controller])
) -> Dict[str, Any]:
    """Get all custom field values for a company candidate"""
    return controller.get_custom_field_values_by_company_candidate(company_candidate_id)


@router.put("/{value_id}", response_model=CustomFieldValueResponse)
@inject
def update_custom_field_value(
    value_id: str,
    request: UpdateCustomFieldValueRequest,
    controller: CustomFieldValueController = Depends(Provide[Container.custom_field_value_controller])
) -> CustomFieldValueResponse:
    """Update a custom field value"""
    result = controller.update_custom_field_value(value_id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Custom field value not found"
        )
    return result


@router.delete("/{value_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_custom_field_value(
    value_id: str,
    controller: CustomFieldValueController = Depends(Provide[Container.custom_field_value_controller])
) -> None:
    """Delete a custom field value"""
    controller.delete_custom_field_value(value_id)
