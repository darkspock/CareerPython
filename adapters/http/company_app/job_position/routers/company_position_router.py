"""Company Position Router - For company users to manage their job positions"""
import base64
import json
import logging
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.security import OAuth2PasswordBearer

from adapters.http.admin_app.controllers.job_position_controller import JobPositionController
from adapters.http.admin_app.schemas.job_position import (
    JobPositionListResponse,
    JobPositionResponse,
)
from adapters.http.admin_app.schemas.job_position_workflow import MoveJobPositionToStageRequest
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/positions", tags=["Company Job Positions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_id from JWT token"""
    try:
        # Decode JWT token (payload is in the second part)
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_id = data.get('company_id')

        if not company_id or not isinstance(company_id, str):
            raise HTTPException(status_code=401, detail="company_id not found in token")

        return str(company_id)
    except Exception as e:
        log.error(f"Error extracting company_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def get_company_user_id_from_token(token: str = Security(oauth2_scheme)) -> Optional[str]:
    """Extract company_user_id from JWT token"""
    try:
        # Decode JWT token (payload is in the second part)
        parts = token.split('.')
        if len(parts) != 3:
            return None

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_user_id = data.get('company_user_id')

        if company_user_id and isinstance(company_user_id, str):
            return str(company_user_id)
        return None
    except Exception:
        return None


@router.get("", response_model=JobPositionListResponse)
@inject
def list_positions(
        controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: Optional[str] = Depends(get_company_user_id_from_token),
        search_term: Optional[str] = Query(None, description="Search in position titles"),
        job_category: Optional[str] = Query(None, description="Filter by job category"),
        visibility: Optional[str] = Query(None, description="Filter by visibility"),
        is_active: Optional[bool] = Query(None, description="Filter by active status"),
        page: Optional[int] = Query(1, ge=1, description="Page number"),
        page_size: Optional[int] = Query(10, ge=1, le=100, description="Items per page")
) -> JobPositionListResponse:
    """List job positions for the authenticated company user"""
    try:
        log.info(f"Listing positions for company_id: {company_id}, company_user_id: {company_user_id}")
        result = controller.list_positions(
            company_id=company_id,
            search_term=search_term,
            department=None,  # Not used in simplified version
            location=None,  # Not used in simplified version
            employment_type=None,  # Not used in simplified version
            experience_level=None,  # Not used in simplified version
            is_remote=None,  # Not used in simplified version
            is_active=is_active,
            page=page,
            page_size=page_size,
            current_user_id=company_user_id
        )
        log.info(f"Found {result.total} positions for company {company_id}")
        return result
    except Exception as e:
        log.error(f"Error listing positions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{position_id}", response_model=JobPositionResponse)
@inject
def get_position(
        position_id: str,
        controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
        company_id: str = Depends(get_company_id_from_token)
) -> JobPositionResponse:
    """Get a specific job position by ID"""
    try:
        position = controller.get_position_by_id(position_id)
        # Verify the position belongs to the company
        if position.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )
        return position
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting position: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{position_id}/move-to-stage", response_model=dict)
@inject
def move_position_to_stage(
        position_id: str,
        request: MoveJobPositionToStageRequest,
        controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: Optional[str] = Depends(get_company_user_id_from_token)
) -> dict:
    """Move a job position to a new stage with validation"""
    from src.company_bc.job_position.application.commands.move_job_position_to_stage import JobPositionValidationError

    try:
        # Verify the position belongs to the company
        position = controller.get_position_by_id(position_id)
        if position.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        # Move the position to the new stage
        return controller.move_position_to_stage(
            position_id=position_id,
            stage_id=request.stage_id,
            comment=request.comment,
            user_id=company_user_id
        )
    except HTTPException:
        raise
    except JobPositionValidationError as e:
        # Return 400 with validation errors
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "validation_errors": e.validation_errors
            }
        )
    except Exception as e:
        log.error(f"Error moving position {position_id} to stage: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
