"""Company Role Router."""
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from adapters.http.company.controllers.company_role_controller import CompanyRoleController
from adapters.http.company.schemas.create_role_request import CreateRoleRequest
from adapters.http.company.schemas.update_role_request import UpdateRoleRequest
from adapters.http.company.schemas.role_response import RoleResponse
from core.container import Container
from src.company_role.domain.exceptions.role_not_found import RoleNotFound
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId

router = APIRouter(prefix="/companies/{company_id}/roles", tags=["Company Roles"])


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company role"
)
@inject
def create_role(
    company_id: str,
    request: CreateRoleRequest,
    controller: Annotated[CompanyRoleController, Depends(Provide[Container.company_role_controller])]
) -> RoleResponse:
    """Create a new role for the company."""
    try:
        return controller.create_role(company_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=List[RoleResponse],
    summary="List company roles"
)
@inject
def list_roles(
    company_id: str,
    controller: Annotated[CompanyRoleController, Depends(Provide[Container.company_role_controller])],
    active_only: bool = False
) -> List[RoleResponse]:
    """List all roles for the company."""
    return controller.list_roles(company_id, active_only)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get role by ID"
)
@inject
def get_role(
    company_id: str,
    role_id: str,
    controller: Annotated[CompanyRoleController, Depends(Provide[Container.company_role_controller])]
) -> RoleResponse:
    """Get a specific role by ID."""
    role = controller.get_role(CompanyRoleId.from_string(role_id))
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {role_id} not found"
        )
    return role


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update a role"
)
@inject
def update_role(
    role_id: str,
    request: UpdateRoleRequest,
    controller: Annotated[CompanyRoleController, Depends(Provide[Container.company_role_controller])]
) -> RoleResponse:
    """Update an existing role."""
    try:
        return controller.update_role(CompanyRoleId.from_string(role_id), request)
    except RoleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role"
)
@inject
def delete_role(
    company_id: str,
    role_id: str,
    controller: Annotated[CompanyRoleController, Depends(Provide[Container.company_role_controller])]
) -> None:
    """Delete a role."""
    try:
        controller.delete_role(role_id)
    except RoleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
