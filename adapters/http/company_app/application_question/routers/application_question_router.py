"""Application Question Router - For managing screening questions on workflows"""
import base64
import json
import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.application_question.controllers.application_question_controller import (
    ApplicationQuestionController
)
from adapters.http.company_app.application_question.schemas.application_question_schemas import (
    ApplicationQuestionListResponse,
    CreateApplicationQuestionRequest,
    UpdateApplicationQuestionRequest
)
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/company/workflows/{workflow_id}/questions",
    tags=["Application Questions"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_id from JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_id = data.get('company_id')

        if not company_id or not isinstance(company_id, str):
            raise HTTPException(status_code=401, detail="company_id not found in token")

        return str(company_id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error extracting company_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get(
    "/",
    response_model=ApplicationQuestionListResponse,
    summary="List application questions for a workflow"
)
@inject
def list_questions(
    workflow_id: str,
    active_only: bool = Query(default=True),
    controller: ApplicationQuestionController = Depends(Provide[Container.application_question_controller]),
    company_id: str = Depends(get_company_id_from_token)
) -> ApplicationQuestionListResponse:
    """List all application questions configured for a workflow"""
    try:
        return controller.list_questions(
            workflow_id=workflow_id,
            active_only=active_only
        )
    except Exception as e:
        log.error(f"Error listing application questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new application question"
)
@inject
def create_question(
    workflow_id: str,
    request: CreateApplicationQuestionRequest,
    controller: ApplicationQuestionController = Depends(Provide[Container.application_question_controller]),
    company_id: str = Depends(get_company_id_from_token)
) -> dict:
    """Create a new application question for a workflow"""
    try:
        question_id = controller.create_question(
            workflow_id=workflow_id,
            company_id=company_id,
            request=request
        )
        return {"id": question_id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error creating application question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an application question"
)
@inject
def update_question(
    workflow_id: str,
    question_id: str,
    request: UpdateApplicationQuestionRequest,
    controller: ApplicationQuestionController = Depends(Provide[Container.application_question_controller]),
    company_id: str = Depends(get_company_id_from_token)
) -> None:
    """Update an application question"""
    try:
        controller.update_question(
            question_id=question_id,
            request=request
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error updating application question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an application question"
)
@inject
def delete_question(
    workflow_id: str,
    question_id: str,
    controller: ApplicationQuestionController = Depends(Provide[Container.application_question_controller]),
    company_id: str = Depends(get_company_id_from_token)
) -> None:
    """Delete an application question"""
    try:
        controller.delete_question(question_id=question_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error deleting application question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
