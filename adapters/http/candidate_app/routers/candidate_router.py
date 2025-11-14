"""
Candidate router - thin routing layer that delegates to controller
All business logic has been moved to CandidateController
"""
import logging
from typing import Optional, List, Annotated, Dict, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from adapters.http.auth.schemas.token import Token
from adapters.http.auth.schemas.user import UserResponse
from adapters.http.auth.services.authentication_service import get_current_user
from core.container import Container
from adapters.http.candidate_app.controllers.application_controller import ApplicationController
from adapters.http.candidate_app.controllers.candidate import CandidateController
from adapters.http.candidate_app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse, \
    CandidateListResponse
from adapters.http.candidate_app.schemas.candidate_education import CandidateEducationResponse, \
    CandidateEducationCreateRequest
from adapters.http.candidate_app.schemas.candidate_experience import CandidateExperienceResponse, \
    CandidateExperienceCreateRequest
from adapters.http.candidate_app.schemas.candidate_job_applications import (
    CandidateJobApplicationSummary,
    JobApplicationListFilters
)
from adapters.http.candidate_app.schemas.candidate_project import CandidateProjectResponse, CandidateProjectCreateRequest
from src.candidate_bc.candidate.application import GetCandidateByUserIdQuery
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.framework.application.query_bus import QueryBus
from src.auth_bc.user.application import AuthenticateUserQuery
from src.auth_bc.user.application.queries.dtos.auth_dto import AuthenticatedUserDto
from src.auth_bc.user.domain.value_objects import UserId

log = logging.getLogger(__name__)

# Router para candidatos
candidate_router = APIRouter(prefix="/candidate", tags=["candidate"])


# ====================================
# CANDIDATE PROFILE ENDPOINTS
# ====================================

@candidate_router.post("/", response_model=CandidateResponse)
@inject
def create_candidate(
        candidate_data: CandidateCreate,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateResponse:
    """Create a new candidate"""
    new_candidate_id = controller.create_candidate(candidate_data, current_user.id)
    return controller.get_candidate(new_candidate_id)


@candidate_router.get("/profile", response_model=CandidateResponse)
@inject
def get_my_candidate_profile(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateResponse:
    """Get authenticated user's candidate profile"""
    return controller.get_my_profile(current_user.id)


@candidate_router.get("/", response_model=CandidateListResponse)
@inject
def list_candidates(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        name: Optional[str] = None,
        phone: Optional[str] = None,
) -> CandidateListResponse:
    """List candidates with optional filters"""
    candidates = controller.list_candidates(name=name, phone=phone)
    return CandidateListResponse(items=candidates)


@candidate_router.put("/profile", response_model=CandidateResponse)
@inject
def update_my_candidate_profile(
        candidate: CandidateUpdate,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateResponse:
    """Update authenticated user's candidate profile"""
    return controller.update_my_profile(current_user.id, candidate)


# ====================================
# EXPERIENCE ENDPOINTS
# ====================================

@candidate_router.get("/experience", response_model=List[CandidateExperienceResponse])
@inject
def get_my_experiences(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> List[CandidateExperienceResponse]:
    """Get authenticated user's experiences"""
    return controller.get_my_experiences(current_user.id)


@candidate_router.post("/experience", response_model=CandidateExperienceResponse)
@inject
def create_my_experience(
        experience: CandidateExperienceCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateExperienceResponse:
    """Create new experience for authenticated user"""
    return controller.create_my_experience(current_user.id, experience)


@candidate_router.get("/experience/{experience_id}", response_model=CandidateExperienceResponse)
@inject
def get_my_experience_by_id(
        experience_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateExperienceResponse:
    """Get experience by ID for authenticated user"""
    return controller.get_my_experience_by_id(current_user.id, experience_id)


@candidate_router.put("/experience/{experience_id}", response_model=CandidateExperienceResponse)
@inject
def update_my_experience(
        experience_id: str,
        experience: CandidateExperienceCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateExperienceResponse:
    """Update experience for authenticated user"""
    return controller.update_my_experience(current_user.id, experience_id, experience)


@candidate_router.delete("/experience/{experience_id}", status_code=204)
@inject
def delete_my_experience(
        experience_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete experience for authenticated user"""
    controller.delete_my_experience(current_user.id, experience_id)


# ====================================
# EDUCATION ENDPOINTS
# ====================================

@candidate_router.get("/education", response_model=List[CandidateEducationResponse])
@inject
def get_my_educations(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> List[CandidateEducationResponse]:
    """Get authenticated user's educations"""
    return controller.get_my_educations(current_user.id)


@candidate_router.post("/education", response_model=CandidateEducationResponse)
@inject
def create_my_education(
        education: CandidateEducationCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateEducationResponse:
    """Create new education for authenticated user"""
    return controller.create_my_education(current_user.id, education)


@candidate_router.get("/education/{education_id}", response_model=CandidateEducationResponse)
@inject
def get_my_education_by_id(
        education_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateEducationResponse:
    """Get education by ID for authenticated user"""
    return controller.get_my_education_by_id(current_user.id, education_id)


@candidate_router.put("/education/{education_id}", response_model=CandidateEducationResponse)
@inject
def update_my_education(
        education_id: str,
        education: CandidateEducationCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateEducationResponse:
    """Update education for authenticated user"""
    return controller.update_my_education(current_user.id, education_id, education)


@candidate_router.delete("/education/{education_id}", status_code=204)
@inject
def delete_my_education(
        education_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete education for authenticated user"""
    controller.delete_my_education(current_user.id, education_id)


# ====================================
# PROJECT ENDPOINTS
# ====================================

@candidate_router.get("/projects", response_model=List[CandidateProjectResponse])
@inject
def get_my_projects(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> List[CandidateProjectResponse]:
    """Get authenticated user's projects"""
    return controller.get_my_projects(current_user.id)


@candidate_router.post("/projects", response_model=CandidateProjectResponse)
@inject
def create_my_project(
        project: CandidateProjectCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateProjectResponse:
    """Create new project for authenticated user"""
    return controller.create_my_project(current_user.id, project)


@candidate_router.get("/projects/{project_id}", response_model=CandidateProjectResponse)
@inject
def get_my_project_by_id(
        project_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateProjectResponse:
    """Get project by ID for authenticated user"""
    return controller.get_my_project_by_id(current_user.id, project_id)


@candidate_router.put("/projects/{project_id}", response_model=CandidateProjectResponse)
@inject
def update_my_project(
        project_id: str,
        project: CandidateProjectCreateRequest,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateProjectResponse:
    """Update project for authenticated user"""
    return controller.update_my_project(current_user.id, project_id, project)


@candidate_router.delete("/projects/{project_id}", status_code=204)
@inject
def delete_my_project(
        project_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete project for authenticated user"""
    controller.delete_my_project(current_user.id, project_id)


# ====================================
# APPLICATION ENDPOINTS
# ====================================

@candidate_router.get("/application", response_model=List[CandidateJobApplicationSummary])
@inject
def get_my_applications(
        controller: Annotated[ApplicationController, Depends(Provide[Container.application_controller])],
        candidate_controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
        status: Optional[str] = None,
        limit: Optional[int] = None,
) -> List[CandidateJobApplicationSummary]:
    """Get applications for authenticated user"""
    candidate = candidate_controller.get_my_profile(current_user.id)

    filters = JobApplicationListFilters(
        status=ApplicationStatusEnum(status) if status else None,
        limit=limit
    )

    return controller.get_applications_by_candidate(candidate.id, filters)


@candidate_router.post("/application", status_code=201)
@inject
def create_application(
        job_position_id: str,
        controller: Annotated[ApplicationController, Depends(Provide[Container.application_controller])],
        candidate_controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
        cover_letter: Optional[str] = None,
) -> dict:
    """Create new application for authenticated user"""
    candidate = candidate_controller.get_my_profile(current_user.id)

    application_id = controller.create_application(
        candidate_id=candidate.id,
        job_position_id=job_position_id,
        cover_letter=cover_letter
    )

    return {
        "application_id": application_id,
        "message": "Application created successfully"
    }


@candidate_router.put("/application/{application_id}/status", status_code=204)
@inject
def update_application_status(
        application_id: str,
        status: str,
        controller: Annotated[ApplicationController, Depends(Provide[Container.application_controller])],
        current_user: UserResponse = Depends(get_current_user),
        notes: Optional[str] = None,
) -> None:
    """Update application status for authenticated user"""
    from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum

    try:
        status_enum = ApplicationStatusEnum(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")

    controller.update_application_status(application_id, status_enum, notes)


# ====================================
# ENHANCED DASHBOARD ENDPOINTS
# ====================================

@candidate_router.get("/profile/summary")
@inject
def get_profile_summary(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get comprehensive profile summary for dashboard"""
    return controller.get_profile_summary(current_user.id)


@candidate_router.post("/experience/bulk", response_model=List[CandidateExperienceResponse])
@inject
def create_multiple_experiences(
        experiences: List[CandidateExperienceCreateRequest],
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> List[CandidateExperienceResponse]:
    """Create multiple experiences at once for better dashboard UX"""
    return controller.create_multiple_experiences(current_user.id, experiences)


@candidate_router.put("/experience/bulk", response_model=List[CandidateExperienceResponse])
@inject
def update_multiple_experiences(
        experience_updates: List[Dict[str, Any]],
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> List[CandidateExperienceResponse]:
    """Update multiple experiences at once for better dashboard UX"""
    return controller.update_multiple_experiences(current_user.id, experience_updates)


@candidate_router.get("/profile/validation")
@inject
def validate_profile_completeness(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> Dict[str, Any]:
    """Validate profile completeness and provide recommendations"""
    return controller.validate_profile_completeness(current_user.id)


@candidate_router.post("/profile/auto-enhance")
@inject
def auto_enhance_profile(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> Dict[str, Any]:
    """Auto-enhance profile with AI suggestions"""
    return controller.auto_enhance_profile(current_user.id)


@candidate_router.post("/upload-resume")
@inject
async def upload_resume_for_ai_processing(
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> Dict[str, Any]:
    """Upload and process resume with AI extraction"""
    try:
        return controller.upload_resume_for_ai_processing(current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "resume_processing_failed",
                "message": "Failed to process uploaded resume",
                "details": str(e)
            }
        )


# ====================================
# GENERIC CANDIDATE ENDPOINTS (MUST BE LAST)
# ====================================

@candidate_router.get("/id/{candidate_id}", response_model=CandidateResponse)
@inject
def get_candidate(
        candidate_id: str,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
        current_user: UserResponse = Depends(get_current_user),
) -> CandidateResponse:
    """Get candidate by ID (with ownership verification)"""
    return controller.get_candidate_with_ownership_check(candidate_id, current_user.id)


@candidate_router.put("/id/{candidate_id}", response_model=CandidateResponse)
@inject
def update_candidate(
        candidate_id: str,
        candidate: CandidateUpdate,
        controller: Annotated[CandidateController, Depends(Provide[Container.candidate_controller])],
) -> CandidateResponse:
    """Update candidate by ID"""
    controller.update_candidate(candidate_id, candidate)
    return controller.get_candidate(candidate_id)


# ====================================
# CANDIDATE AUTH ENDPOINTS
# ====================================

@candidate_router.post("/auth/login", response_model=Token)
@inject
def candidate_login(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Authenticate candidate user and return JWT token"""
    try:
        # Use the authentication query to validate credentials and get token
        query = AuthenticateUserQuery(email=form_data.username, password=form_data.password)
        auth_result: Optional[AuthenticatedUserDto] = query_bus.query(query)

        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Look up candidate profile for this user
        candidate_id = None
        try:
            user_id = UserId.from_string(auth_result.user_id)
            candidate_query = GetCandidateByUserIdQuery(user_id=user_id)
            candidate_dto: Optional[CandidateDto] = query_bus.query(candidate_query)
            if candidate_dto:
                candidate_id = candidate_dto.id.value
        except Exception:
            # If candidate lookup fails, continue without candidate_id
            pass

        return Token(
            access_token=auth_result.access_token,
            token_type=auth_result.token_type,
            expires_in=2880 * 60,  # 48 hours in seconds
            candidate_id=candidate_id
        )

    except Exception as e:
        log.error(f"Candidate authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@candidate_router.get("/auth/me", response_model=UserResponse)
def get_current_candidate_user(
        current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """Get current candidate user info from JWT token"""
    return current_user
