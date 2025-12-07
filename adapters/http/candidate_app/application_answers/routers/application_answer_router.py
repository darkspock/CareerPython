"""Application Answer Router - For managing question answers on applications"""
import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from adapters.http.candidate_app.application_answers.controllers.application_answer_controller import (
    ApplicationAnswerController
)
from adapters.http.candidate_app.application_answers.schemas.application_answer_schemas import (
    SaveAnswersRequest,
    ApplicationAnswerListResponse,
    EnabledQuestionsListResponse
)
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/applications",
    tags=["Application Answers"]
)

# Separate router for public endpoints (get enabled questions)
public_router = APIRouter(
    prefix="/api/public/positions",
    tags=["Public Application Questions"]
)


@router.get(
    "/{application_id}/answers",
    response_model=ApplicationAnswerListResponse,
    summary="List answers for an application"
)
@inject
def list_answers(
    application_id: str,
    controller: ApplicationAnswerController = Depends(Provide[Container.application_answer_controller])
) -> ApplicationAnswerListResponse:
    """List all question answers for an application."""
    try:
        return controller.list_answers(application_id=application_id)
    except Exception as e:
        log.error(f"Error listing application answers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/{application_id}/answers",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Save answers for an application"
)
@inject
def save_answers(
    application_id: str,
    request: SaveAnswersRequest,
    controller: ApplicationAnswerController = Depends(Provide[Container.application_answer_controller])
) -> None:
    """Save question answers for an application."""
    try:
        controller.save_answers(application_id=application_id, request=request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error saving application answers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@public_router.get(
    "/{position_id}/questions",
    response_model=EnabledQuestionsListResponse,
    summary="Get enabled questions for a position (public)"
)
@inject
def get_enabled_questions(
    position_id: str,
    controller: ApplicationAnswerController = Depends(Provide[Container.application_answer_controller])
) -> EnabledQuestionsListResponse:
    """
    Get all enabled questions for a job position.

    This endpoint is public and used by the application form to display
    the screening questions candidates need to answer.
    """
    try:
        return controller.get_enabled_questions(position_id=position_id)
    except Exception as e:
        log.error(f"Error getting enabled questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
