"""Router for company operations on candidate applications"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from core.container import Container
from adapters.http.candidate.controllers.application_controller import ApplicationController


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
