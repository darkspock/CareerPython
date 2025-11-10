"""
Resume router with full resume generation functionality
"""
import logging
from typing import Dict, Any, Optional, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from adapters.http.auth.schemas.user import UserResponse
from adapters.http.candidate_app.schemas.resume_request import CreateGeneralResumeRequest, UpdateResumeContentRequest, \
    UpdateResumeNameRequest, BulkDeleteResumesRequest
from adapters.http.candidate_app.schemas.resume_response import ResumeListResponse, ResumeResponse, ResumeStatisticsResponse
from core.container import Container
from adapters.http.candidate_app.controllers.resume_controller import ResumeController
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="candidate/auth/login")

# Router for resume endpoints - MOVED to /candidate/resume per FIX1.md
router = APIRouter(prefix="/candidate/resume", tags=["candidate-resume"])


# Test endpoint without authentication for development
@router.get("/test/candidate/{candidate_id}", response_model=ResumeListResponse)
@inject
async def test_get_resumes_by_candidate(
        candidate_id: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        resume_type: Optional[str] = None,
        limit: Optional[int] = None
) -> ResumeListResponse:
    """Test endpoint to get resumes by candidate ID without authentication"""
    try:
        return controller.get_resumes(
            candidate_id=candidate_id,
            resume_type=resume_type,
            limit=limit
        )
    except Exception as e:
        log.error(f"Error getting resumes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve resumes: {str(e)}"
        )


@router.get("/test/{resume_id}/content", response_model=ResumeResponse)
@inject
async def test_get_resume_content(
        resume_id: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])]
) -> ResumeResponse:
    """Test endpoint to get resume content without authentication"""
    try:
        return controller.get_resume_by_id(resume_id)
    except Exception as e:
        log.error(f"Error getting resume content: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve resume content: {str(e)}"
        )


@router.post("/test/candidate/{candidate_id}", response_model=ResumeResponse)
@inject
async def test_create_resume_for_candidate(
        candidate_id: str,
        request: CreateGeneralResumeRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])]
) -> ResumeResponse:
    """Test endpoint to create resume for specific candidate without authentication"""
    try:
        # Pass candidate_id from URL parameter
        log.info(f"TEST: Creating resume for candidate {candidate_id}")
        return controller.create_general_resume(candidate_id, request)
    except Exception as e:
        log.error(f"Error creating test resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create resume: {str(e)}"
        )


@inject
def get_current_user(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        token: str = Security(oauth2_scheme),
) -> UserResponse:
    """Get current user from JWT token"""
    try:
        from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery
        from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto

        query = GetCurrentUserFromTokenQuery(token=token)
        user_dto: CurrentUserDto = query_bus.query(query)
        if not user_dto:
            raise HTTPException(status_code=401, detail="Invalid token")

        return UserResponse(
            id=str(user_dto.user_id),
            email=user_dto.email,
            is_active=user_dto.is_active,
            subscription_tier="FREE"  # Default value
        )
    except Exception as e:
        log.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/", response_model=ResumeListResponse)
@inject
async def get_resumes(
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        resume_type: Optional[str] = None,
        limit: Optional[int] = None,
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeListResponse:
    """Get list of resumes for the current user"""
    try:
        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")

        return controller.get_resumes(
            candidate_id=candidate.id,
            resume_type=resume_type,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting resumes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve resumes: {str(e)}"
        )


@router.get("/stats", response_model=ResumeStatisticsResponse)
@inject
async def get_resume_stats(
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeStatisticsResponse:
    """Get resume statistics for the current user"""
    try:
        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")

        return controller.get_resume_statistics(candidate.id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting resume statistics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


@router.get("/{resume_id}", response_model=ResumeResponse)
@inject
async def get_resume_by_id(
        resume_id: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Get resume by ID"""
    try:
        resume = controller.get_resume_by_id(resume_id)

        # Verify ownership - get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate or resume.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Resume not found or unauthorized")

        return resume
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting resume by ID: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve resume: {str(e)}"
        )


@router.get("/{resume_id}/content", response_model=ResumeResponse)
@inject
async def get_resume_content(
        resume_id: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Get resume content by ID (same as get_resume_by_id for now)"""
    return await get_resume_by_id(resume_id=resume_id, controller=controller, current_user=current_user)


@router.post("/", response_model=ResumeResponse)
@inject
async def create_resume(
        request: CreateGeneralResumeRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Create a new resume"""
    try:
        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")

        # Pass candidate_id from authentication context
        return controller.create_general_resume(candidate.id, request)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error creating resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create resume: {str(e)}"
        )


@router.post("/general", response_model=ResumeResponse)
@inject
async def create_general_resume(
        request: CreateGeneralResumeRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Create a general resume"""
    try:
        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")

        # Pass candidate_id from authentication context
        log.info(f"Creating general resume for candidate {candidate.id}, user {current_user.id}")
        return controller.create_general_resume(candidate.id, request)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error creating general resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create general resume: {str(e)}"
        )


@router.put("/{resume_id}/content", response_model=ResumeResponse)
@inject
async def update_resume_content(
        resume_id: str,
        request: UpdateResumeContentRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Update resume content"""
    try:
        # First verify ownership
        resume = controller.get_resume_by_id(resume_id)

        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate or resume.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Resume not found or unauthorized")

        return controller.update_resume_content(resume_id, request)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating resume content: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update resume content: {str(e)}"
        )


@router.put("/{resume_id}/name", response_model=ResumeResponse)
@inject
async def update_resume_name(
        resume_id: str,
        request: UpdateResumeNameRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Update resume name"""
    try:
        # First verify ownership
        resume = controller.get_resume_by_id(resume_id)

        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate or resume.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Resume not found or unauthorized")

        return controller.get_resume_by_id(resume_id)  # Return current resume for now
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating resume name: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update resume name: {str(e)}"
        )


@router.delete("/{resume_id}")
@inject
async def delete_resume(
        resume_id: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete resume"""
    try:
        # First verify ownership
        resume = controller.get_resume_by_id(resume_id)

        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate or resume.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Resume not found or unauthorized")

        return controller.delete_resume(resume_id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete resume: {str(e)}"
        )


@router.post("/{resume_id}/duplicate", response_model=ResumeResponse)
@inject
async def duplicate_resume(
        resume_id: str,
        new_name: str,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> ResumeResponse:
    """Duplicate resume (simplified implementation)"""
    try:
        # First verify ownership and get original resume
        original_resume = controller.get_resume_by_id(resume_id)

        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate or original_resume.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Resume not found or unauthorized")

        # Create a new resume based on the original
        duplicate_request = CreateGeneralResumeRequest(
            name=new_name,
            include_ai_enhancement=False,  # Don't duplicate AI enhancement
            general_data=original_resume.general_data
        )

        return controller.create_general_resume(candidate.id, duplicate_request)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error duplicating resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to duplicate resume: {str(e)}"
        )


@router.post("/bulk-delete")
@inject
async def bulk_delete_resumes(
        request: BulkDeleteResumesRequest,
        controller: Annotated[ResumeController, Depends(Provide[Container.resume_controller])],
        current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """Bulk delete resumes"""
    try:
        # Get candidate profile for current user
        from adapters.http.candidate_app.controllers.candidate import CandidateController
        from core.container import Container as ContainerRef

        candidate_controller = ContainerRef.candidate_controller()
        candidate = candidate_controller.get_candidate_by_user_id(current_user.id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")

        deleted_count = 0
        failed_deletes = []

        for resume_id in request.resume_ids:
            try:
                # Verify ownership first
                resume = controller.get_resume_by_id(resume_id)
                if resume.candidate_id != candidate.id:
                    failed_deletes.append(resume_id)
                    continue

                controller.delete_resume(resume_id)
                deleted_count += 1
            except Exception as e:
                log.error(f"Failed to delete resume {resume_id}: {e}")
                failed_deletes.append(resume_id)

        return {
            "deleted_count": deleted_count,
            "failed_deletes": failed_deletes,
            "total_requested": len(request.resume_ids),
            "message": f"Successfully deleted {deleted_count} resumes"
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error in bulk delete resumes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete resumes: {str(e)}"
        )
