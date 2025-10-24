from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from core.container import Container
from src.company_workflow.presentation.controllers.company_workflow_controller import CompanyWorkflowController
from src.company_workflow.presentation.schemas.company_workflow_response import CompanyWorkflowResponse
from src.company_workflow.presentation.schemas.create_workflow_request import CreateWorkflowRequest
from src.company_workflow.presentation.schemas.update_workflow_request import UpdateWorkflowRequest

router = APIRouter(
    prefix="/api/company-workflows",
    tags=["company-workflows"]
)


@router.post(
    "/",
    response_model=CompanyWorkflowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workflow"
)
@inject
def create_workflow(
        request: CreateWorkflowRequest,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Create a new workflow"""
    try:
        return controller.create_workflow(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{workflow_id}",
    response_model=CompanyWorkflowResponse,
    summary="Get a workflow by ID"
)
@inject
def get_workflow_by_id(
        workflow_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> Optional[CompanyWorkflowResponse]:
    """Get a workflow by ID"""
    result = controller.get_workflow_by_id(workflow_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return result


@router.get(
    "/company/{company_id}",
    response_model=List[CompanyWorkflowResponse],
    summary="List all workflows for a company"
)
@inject
def list_workflows_by_company(
        company_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> List[CompanyWorkflowResponse]:
    """List all workflows for a company"""
    return controller.list_workflows_by_company(company_id)


@router.put(
    "/{workflow_id}",
    response_model=CompanyWorkflowResponse,
    summary="Update workflow information"
)
@inject
def update_workflow(
        workflow_id: str,
        request: UpdateWorkflowRequest,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Update workflow information"""
    try:
        return controller.update_workflow(workflow_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/activate",
    response_model=CompanyWorkflowResponse,
    summary="Activate a workflow"
)
@inject
def activate_workflow(
        workflow_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Activate a workflow"""
    try:
        return controller.activate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/deactivate",
    response_model=CompanyWorkflowResponse,
    summary="Deactivate a workflow"
)
@inject
def deactivate_workflow(
        workflow_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Deactivate a workflow"""
    try:
        return controller.deactivate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/archive",
    response_model=CompanyWorkflowResponse,
    summary="Archive a workflow"
)
@inject
def archive_workflow(
        workflow_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Archive a workflow"""
    try:
        return controller.archive_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/set-default",
    response_model=CompanyWorkflowResponse,
    summary="Set a workflow as default"
)
@inject
def set_as_default_workflow(
        workflow_id: str,
        company_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Set a workflow as default for a company"""
    try:
        return controller.set_as_default_workflow(workflow_id, company_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/unset-default",
    response_model=CompanyWorkflowResponse,
    summary="Unset a workflow as default"
)
@inject
def unset_as_default_workflow(
        workflow_id: str,
        controller: CompanyWorkflowController = Depends(Provide[Container.company_workflow_controller])
) -> CompanyWorkflowResponse:
    """Unset a workflow as default"""
    try:
        return controller.unset_as_default_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
