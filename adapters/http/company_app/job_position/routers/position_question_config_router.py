"""Position Question Config Router - For managing question configurations per job position"""
import base64
import json
import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.job_position.controllers.position_question_config_controller import (
    PositionQuestionConfigController
)
from adapters.http.company_app.job_position.schemas.position_question_config_schemas import (
    ConfigurePositionQuestionRequest,
    PositionQuestionConfigListResponse
)
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/company/positions/{position_id}/questions",
    tags=["Position Question Config"]
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
    response_model=PositionQuestionConfigListResponse,
    summary="List question configurations for a position"
)
@inject
def list_configs(
    position_id: str,
    enabled_only: bool = Query(default=False),
    controller: PositionQuestionConfigController = Depends(
        Provide[Container.position_question_config_controller]
    ),
    company_id: str = Depends(get_company_id_from_token)
) -> PositionQuestionConfigListResponse:
    """List all question configurations for a job position."""
    try:
        return controller.list_configs(
            position_id=position_id,
            enabled_only=enabled_only
        )
    except Exception as e:
        log.error(f"Error listing position question configs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Configure a question for a position"
)
@inject
def configure_question(
    position_id: str,
    request: ConfigurePositionQuestionRequest,
    controller: PositionQuestionConfigController = Depends(
        Provide[Container.position_question_config_controller]
    ),
    company_id: str = Depends(get_company_id_from_token)
) -> None:
    """Configure a question for a job position (enable/disable, set overrides)."""
    try:
        controller.configure_question(
            position_id=position_id,
            request=request
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error configuring position question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a question configuration from a position"
)
@inject
def remove_config(
    position_id: str,
    question_id: str,
    controller: PositionQuestionConfigController = Depends(
        Provide[Container.position_question_config_controller]
    ),
    company_id: str = Depends(get_company_id_from_token)
) -> None:
    """Remove a question configuration from a position, reverting to workflow defaults."""
    try:
        controller.remove_config(
            position_id=position_id,
            question_id=question_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error removing position question config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
