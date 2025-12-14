"""Registration Router - Email verification based registration flow"""
import logging
from typing import Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, Query
from pydantic import BaseModel

from adapters.http.candidate_app.controllers.registration_controller import RegistrationController
from core.containers import Container

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidate/registration", tags=["candidate-registration"])


class InitiateRegistrationResponse(BaseModel):
    success: bool
    message: str
    registration_id: str


class VerifyRegistrationResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    candidate_id: Optional[str] = None
    is_new_user: bool = False
    has_job_application: bool = False
    access_token: Optional[str] = None
    redirect_url: str


class RegistrationStatusResponse(BaseModel):
    registration_id: str
    status: str
    processing_status: str
    is_verified: bool
    is_expired: bool
    has_pdf: bool
    preview_data: Optional[dict] = None


@router.post("", response_model=InitiateRegistrationResponse)
@inject
async def initiate_registration(
        *,
        email: str = Form(...),
        company_id: Optional[str] = Form(None),
        job_position_id: Optional[str] = Form(None),
        resume_file: Optional[UploadFile] = File(None),
        gdpr_consent: bool = Form(...),
        registration_controller: Annotated[
            RegistrationController,
            Depends(Provide[Container.registration_controller])
        ],
) -> InitiateRegistrationResponse:
    """
    Initiate registration process with email verification.

    - Validates GDPR consent
    - Creates a pending registration
    - Sends verification email
    - Starts PDF processing in background (if provided)
    """
    result = await registration_controller.initiate_registration(
        email=email,
        company_id=company_id,
        job_position_id=job_position_id,
        resume_file=resume_file,
        gdpr_consent=gdpr_consent
    )
    return InitiateRegistrationResponse(**result)


@router.get("/verify/{token}", response_model=VerifyRegistrationResponse)
@inject
async def verify_registration(
        token: str,
        registration_controller: Annotated[
            RegistrationController,
            Depends(Provide[Container.registration_controller])
        ],
) -> VerifyRegistrationResponse:
    """
    Verify registration using email token.

    - Creates user and candidate (or links to existing)
    - Creates job application if job_position_id was provided
    - Returns JWT token for authentication
    - Returns redirect URL (wizard or profile)
    """
    result = await registration_controller.verify_registration(token)
    return VerifyRegistrationResponse(**result)


@router.get("/{registration_id}/status", response_model=RegistrationStatusResponse)
@inject
async def get_registration_status(
        registration_id: str,
        registration_controller: Annotated[
            RegistrationController,
            Depends(Provide[Container.registration_controller])
        ],
) -> RegistrationStatusResponse:
    """
    Get registration status and PDF processing progress.

    - Returns current status (PENDING, VERIFIED, EXPIRED)
    - Returns processing status (PENDING, PROCESSING, COMPLETED, FAILED)
    - Returns preview data from PDF extraction
    """
    result = await registration_controller.get_registration_status(registration_id)
    return RegistrationStatusResponse(**result)
