from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status

from adapters.http.shared.workflow.controllers import WorkflowController
from adapters.http.shared.workflow.schemas import CreateWorkflowRequest
from adapters.http.shared.workflow.schemas import WorkflowResponse
from adapters.http.shared.workflow.schemas.update_workflow_request import UpdateWorkflowRequest
from core.containers import Container

router = APIRouter(
    prefix="/api/company-workflows",
    tags=["company-workflows"]
)


@router.post(
    "/",
    response_model=WorkflowResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workflow"
)
@inject
def create_workflow(
        request: CreateWorkflowRequest,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Create a new workflow"""
    try:
        return controller.create_workflow(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse,
    summary="Get a workflow by ID"
)
@inject
def get_workflow_by_id(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> Optional[WorkflowResponse]:
    """Get a workflow by ID"""
    result = controller.get_workflow_by_id(workflow_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return result


@router.get(
    "/company/{company_id}",
    response_model=List[WorkflowResponse],
    summary="List all workflows for a company"
)
@inject
def list_workflows_by_company(
        company_id: str,
        workflow_type: Optional[str] = Query(None, description="Filter by workflow type (CA, PO, CO)"),
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> List[WorkflowResponse]:
    """List all workflows for a company"""
    return controller.list_workflows_by_company(company_id, workflow_type)


@router.get(
    "/",
    response_model=List[WorkflowResponse],
    summary="List workflows with filters"
)
@inject
def list_workflows(
        phase_id: Optional[str] = Query(None, description="Filter by phase ID"),
        workflow_type: Optional[str] = Query(None, description="Filter by workflow type (CA, PO, CO)"),
        workflow_status: Optional[str] = Query(None, description="Filter by status (active, draft, archived)"),
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> List[WorkflowResponse]:
    """List workflows filtered by phase_id, workflow_type and/or status

    Args:
        phase_id: Optional phase ID to filter workflows
        workflow_type: Optional workflow type (CA, PO, CO). If phase_id is provided, workflow_type is optional.
        workflow_status: Optional status to filter workflows (active, draft, archived)

    Returns:
        List of workflows matching the filters
    """
    if phase_id:
        # If phase_id is provided, workflow_type is optional
        try:
            return controller.list_workflows_by_phase(phase_id, workflow_type, workflow_status)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        # If no phase_id, require company_id and optionally workflow_type
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="phase_id query parameter is required. Use /company/{company_id} endpoint to list workflows by company."
        )


@router.put(
    "/{workflow_id}",
    response_model=WorkflowResponse,
    summary="Update workflow information"
)
@inject
def update_workflow(
        workflow_id: str,
        request: UpdateWorkflowRequest,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Update workflow information"""
    try:
        return controller.update_workflow(workflow_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/activate",
    response_model=WorkflowResponse,
    summary="Activate a workflow"
)
@inject
def activate_workflow(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Activate a workflow"""
    try:
        return controller.activate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/deactivate",
    response_model=WorkflowResponse,
    summary="Deactivate a workflow"
)
@inject
def deactivate_workflow(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Deactivate a workflow"""
    try:
        return controller.deactivate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/archive",
    response_model=WorkflowResponse,
    summary="Archive a workflow"
)
@inject
def archive_workflow(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Archive a workflow"""
    try:
        return controller.archive_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/set-default",
    response_model=WorkflowResponse,
    summary="Set a workflow as default"
)
@inject
def set_as_default_workflow(
        workflow_id: str,
        company_id: str = Query(..., description="Company ID"),
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Set a workflow as default for a company"""
    try:
        return controller.set_as_default_workflow(workflow_id, company_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{workflow_id}/unset-default",
    response_model=WorkflowResponse,
    summary="Unset a workflow as default"
)
@inject
def unset_as_default_workflow(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Unset a workflow as default"""
    try:
        return controller.unset_as_default_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workflow"
)
@inject
def delete_workflow(
        workflow_id: str,
        controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> None:
    """Delete a workflow permanently"""
    try:
        controller.delete_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
