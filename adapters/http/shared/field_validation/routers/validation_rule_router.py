from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query

from adapters.http.shared.field_validation.controllers.validation_rule_controller import ValidationRuleController
from adapters.http.shared.field_validation.schemas.create_validation_rule_request import CreateValidationRuleRequest
from adapters.http.shared.field_validation.schemas.update_validation_rule_request import UpdateValidationRuleRequest
from adapters.http.shared.field_validation.schemas.validate_stage_request import ValidateStageRequest
from adapters.http.shared.field_validation.schemas.validation_result_response import ValidationResultResponse
from adapters.http.shared.field_validation.schemas.validation_rule_response import ValidationRuleResponse
from core.containers import Container

router = APIRouter(
    prefix="/validation-rules",
    tags=["validation-rules"]
)


@router.post("", response_model=ValidationRuleResponse, status_code=201)
@inject
def create_validation_rule(
        request: CreateValidationRuleRequest,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationRuleResponse:
    """Create a new validation rule."""
    try:
        return controller.create_validation_rule(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{rule_id}", response_model=ValidationRuleResponse)
@inject
def get_validation_rule(
        rule_id: str,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationRuleResponse:
    """Get a validation rule by ID."""
    try:
        return controller.get_validation_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stage/{stage_id}", response_model=List[ValidationRuleResponse])
@inject
def list_validation_rules_by_stage(
        stage_id: str,
        active_only: bool = Query(False, description="Filter only active rules"),
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> List[ValidationRuleResponse]:
    """List all validation rules for a workflow stage."""
    try:
        return controller.list_validation_rules_by_stage(stage_id, active_only)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/field/{custom_field_id}", response_model=List[ValidationRuleResponse])
@inject
def list_validation_rules_by_field(
        custom_field_id: str,
        active_only: bool = Query(False, description="Filter only active rules"),
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> List[ValidationRuleResponse]:
    """List all validation rules for a custom field."""
    try:
        return controller.list_validation_rules_by_field(custom_field_id, active_only)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{rule_id}", response_model=ValidationRuleResponse)
@inject
def update_validation_rule(
        rule_id: str,
        request: UpdateValidationRuleRequest,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationRuleResponse:
    """Update a validation rule."""
    try:
        return controller.update_validation_rule(rule_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{rule_id}", status_code=204)
@inject
def delete_validation_rule(
        rule_id: str,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> None:
    """Delete a validation rule."""
    try:
        controller.delete_validation_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{rule_id}/activate", response_model=ValidationRuleResponse)
@inject
def activate_validation_rule(
        rule_id: str,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationRuleResponse:
    """Activate a validation rule."""
    try:
        return controller.activate_validation_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{rule_id}/deactivate", response_model=ValidationRuleResponse)
@inject
def deactivate_validation_rule(
        rule_id: str,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationRuleResponse:
    """Deactivate a validation rule."""
    try:
        return controller.deactivate_validation_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate-stage", response_model=ValidationResultResponse)
@inject
def validate_stage_transition(
        request: ValidateStageRequest,
        controller: ValidationRuleController = Depends(Provide[Container.validation_rule_controller])
) -> ValidationResultResponse:
    """Validate a candidate's field values for a stage transition."""
    try:
        return controller.validate_stage_transition(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
