from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from core.container import Container
from adapters.http.customization.controllers.entity_customization_controller import EntityCustomizationController
from adapters.http.customization.schemas.create_entity_customization_request import CreateEntityCustomizationRequest
from adapters.http.customization.schemas.update_entity_customization_request import UpdateEntityCustomizationRequest
from adapters.http.customization.schemas.entity_customization_response import EntityCustomizationResponse

router = APIRouter(
    prefix="/api/entity-customizations",
    tags=["entity-customizations"]
)


@router.post(
    "",
    response_model=EntityCustomizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new entity customization"
)
@inject
def create_entity_customization(
    request: CreateEntityCustomizationRequest,
    controller: EntityCustomizationController = Depends(Provide[Container.entity_customization_controller])
) -> EntityCustomizationResponse:
    """Create a new entity customization"""
    try:
        return controller.create_entity_customization(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/by-id/{id}",
    response_model=EntityCustomizationResponse,
    summary="Get entity customization by ID"
)
@inject
def get_entity_customization_by_id(
    id: str,
    controller: EntityCustomizationController = Depends(Provide[Container.entity_customization_controller])
) -> EntityCustomizationResponse:
    """Get an entity customization by ID"""
    result = controller.get_entity_customization_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity customization not found"
        )
    return result


@router.get(
    "/{entity_type}/{entity_id}",
    response_model=EntityCustomizationResponse,
    summary="Get entity customization by entity type and entity ID"
)
@inject
def get_entity_customization(
    entity_type: str,
    entity_id: str,
    controller: EntityCustomizationController = Depends(Provide[Container.entity_customization_controller])
) -> EntityCustomizationResponse:
    """Get an entity customization by entity type and entity ID
    
    Valid entity_type values: JobPosition, CandidateApplication, Candidate, Workflow
    """
    try:
        result = controller.get_entity_customization(entity_type, entity_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity customization not found"
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put(
    "/{id}",
    response_model=EntityCustomizationResponse,
    summary="Update an entity customization"
)
@inject
def update_entity_customization(
    id: str,
    request: UpdateEntityCustomizationRequest,
    controller: EntityCustomizationController = Depends(Provide[Container.entity_customization_controller])
) -> EntityCustomizationResponse:
    """Update an entity customization"""
    try:
        return controller.update_entity_customization(id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an entity customization"
)
@inject
def delete_entity_customization(
    id: str,
    controller: EntityCustomizationController = Depends(Provide[Container.entity_customization_controller])
) -> None:
    """Delete an entity customization"""
    try:
        controller.delete_entity_customization(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

