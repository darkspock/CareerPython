import logging
from typing import Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Security
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from adapters.http.candidate.controllers.onboarding_controller import OnboardingController
from adapters.http.candidate.schemas.onboarding import LandingResponse
from core.container import Container
from src.shared.application.query_bus import QueryBus
from src.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidate/onboarding", tags=["candidate-onboarding"])

# REMOVED: candidates_router - consolidated into main candidate_router
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="candidate/auth/login")


@router.post("/landing", response_model=LandingResponse)
@inject
async def process_landing(
        *,
        email: str = Form(...),
        job_position_id: Optional[str] = Form(None),
        resume_file: Optional[UploadFile] = File(None),
        onboarding_controller: Annotated[OnboardingController, Depends(Provide[Container.onboarding_controller])],
) -> LandingResponse:
    """Process landing page form with optional resume and job application"""
    return await onboarding_controller.process_landing(
        email=email,
        job_position_id=job_position_id,
        resume_file=resume_file
    )


@router.post("/subscribe")
async def subscribe_to_landing(name: str, email: str) -> JSONResponse:
    """Simple subscription endpoint for leads"""
    return JSONResponse(
        status_code=200,
        content={"message": "Suscripción exitosa", "name": name, "email": email}
    )


# Helper function to get current user
@inject
def get_current_user(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        token: str = Security(oauth2_scheme),
) -> CurrentUserDto:
    """Get current user from JWT token"""
    try:
        query = GetCurrentUserFromTokenQuery(token=token)
        user_dto: CurrentUserDto = query_bus.query(query)
        if not user_dto:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_dto
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

# REMOVED: Endpoint moved to main candidate_router - create_candidate function
# This functionality is now available at /candidate/ (POST)


# REMOVED: Endpoint moved to main candidate_router - update_my_profile function
# This functionality is now available at /candidate/profile (PUT)
