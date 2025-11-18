"""Router for company operations on candidate applications"""
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from adapters.http.candidate_app.controllers.application_controller import ApplicationController
from core.containers import Container

router = APIRouter(
    prefix="/api/company/candidate-applications",
    tags=["company-candidate-applications"]
)


class AssignCandidateToPositionRequest(BaseModel):
    """Request to assign a candidate to a position"""
    candidate_id: str
    job_position_id: str


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
def assign_candidate_to_position(
        request: AssignCandidateToPositionRequest,
        controller: Annotated[ApplicationController, Depends(Provide[Container.application_controller])]
) -> dict:
    """
    Company assigns a candidate to a position by creating a candidate_application.
    This is for company-initiated assignments, not candidate-initiated applications.
    """
    try:
        application_id = controller.create_application(
            candidate_id=request.candidate_id,
            job_position_id=request.job_position_id,
            cover_letter=None  # Company assignment doesn't have cover letter
        )

        return {
            "application_id": application_id,
            "message": "Candidate assigned to position successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to assign candidate: {str(e)}"
        )


@router.get("/{application_id}/can-process", status_code=status.HTTP_200_OK)
@inject
def check_user_can_process_application(
        application_id: str,
        user_id: str,  # TODO: Get from auth token/session
        company_id: str,  # TODO: Get from auth token/session
        controller: Annotated[ApplicationController, Depends(Provide[Container.application_controller])]
) -> dict:
    """
    Check if the current user has permission to process an application at its current stage.
    Returns a boolean indicating whether the user can process the application.

    Phase 5: Stage Permissions - This endpoint validates if a user is assigned to the current stage.
    """
    try:
        can_process = controller.can_user_process_application(
            user_id=user_id,
            application_id=application_id,
            company_id=company_id
        )

        return {
            "can_process": can_process,
            "application_id": application_id,
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check permissions: {str(e)}"
        )
