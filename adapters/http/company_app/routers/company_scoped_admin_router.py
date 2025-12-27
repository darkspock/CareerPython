"""
Company-scoped admin routes.

All routes in this router require a company_slug in the URL path.
Only staff members of the company can access these routes.

URL Pattern: /{company_slug}/admin/*
"""
import logging
from typing import List, Optional, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from adapters.http.admin_app.controllers.job_position_controller import JobPositionController
from adapters.http.company_app.company_candidate.controllers.company_candidate_controller import (
    CompanyCandidateController
)
from adapters.http.company_app.company_candidate.schemas.assign_workflow_request import AssignWorkflowRequest
from adapters.http.company_app.company_candidate.schemas.change_stage_request import ChangeStageRequest
from adapters.http.company_app.company_candidate.schemas.company_candidate_response import CompanyCandidateResponse
from adapters.http.company_app.company_candidate.schemas.create_company_candidate_request import (
    CreateCompanyCandidateRequest
)
from adapters.http.company_app.company_candidate.schemas.update_company_candidate_request import (
    UpdateCompanyCandidateRequest
)
from adapters.http.candidate_app.controllers.application_controller import ApplicationController
from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.company_app.interview.schemas.interview_management import (
    InterviewCreateRequest, InterviewUpdateRequest,
    InterviewResource, InterviewFullResource, InterviewListResource, InterviewStatsResource,
    InterviewActionResource, StartInterviewRequest, FinishInterviewRequest
)
from adapters.http.admin_app.controllers.inverview_template_controller import InterviewTemplateController
from adapters.http.admin_app.schemas.interview_template import (
    InterviewTemplateResponse, InterviewTemplateCreate
)
from adapters.http.shared.workflow.controllers import WorkflowController, WorkflowStageController
from adapters.http.shared.workflow.schemas import (
    CreateWorkflowRequest, WorkflowResponse, UpdateWorkflowRequest,
    CreateStageRequest, UpdateStageRequest, WorkflowStageResponse,
    ReorderStagesRequest
)
from adapters.http.company_app.company.controllers.candidate_comment_controller import CandidateCommentController
from adapters.http.company_app.company_candidate.schemas.candidate_comment_response import CandidateCommentResponse
from adapters.http.company_app.company_candidate.schemas.create_candidate_comment_request import (
    CreateCandidateCommentRequest
)
from adapters.http.company_app.company_candidate.schemas.update_candidate_comment_request import (
    UpdateCandidateCommentRequest
)
from adapters.http.company_app.candidate_review.schemas.create_review_request import CreateReviewRequest
from adapters.http.company_app.candidate_review.schemas.review_response import ReviewResponse
from adapters.http.company_app.candidate_review.schemas.update_review_request import UpdateReviewRequest
from adapters.http.company_app.company.controllers.review_controller import ReviewController
from datetime import datetime
from adapters.http.admin_app.schemas.job_position import (
    JobPositionListResponse,
    JobPositionResponse,
    JobPositionActionResponse,
    JobPositionCreate,
    JobPositionUpdate,
    RejectJobPositionRequest,
    CloseJobPositionRequest,
    CreateInlineScreeningTemplateRequest,
    CreateInlineScreeningTemplateResponse,
)
from adapters.http.admin_app.schemas.job_position_workflow import MoveJobPositionToStageRequest
from adapters.http.shared.dependencies.company_context import (
    AdminCompanyContext,
    CurrentCompanyUser,
)
from core.containers import Container
from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# Router with company_slug prefix for admin routes
router = APIRouter(
    prefix="/{company_slug}/admin",
    tags=["Company-Scoped Admin"],
)


# ==================== POSITION MANAGEMENT ====================

@router.get("/positions", response_model=JobPositionListResponse)
@inject
def list_positions(
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
    search_term: Optional[str] = Query(None, description="Search in position titles"),
    job_category: Optional[str] = Query(None, description="Filter by job category"),
    visibility: Optional[str] = Query(None, description="Filter by visibility"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    page_size: Optional[int] = Query(10, ge=1, le=100, description="Items per page")
) -> JobPositionListResponse:
    """List job positions for the company (admin view)"""
    try:
        log.info(f"Listing positions for company: {company.slug}, user: {company_user.id}")
        result = controller.list_positions(
            company_id=company.id,
            search_term=search_term,
            department=None,
            location=None,
            employment_type=None,
            experience_level=None,
            is_remote=None,
            is_active=is_active,
            page=page,
            page_size=page_size,
            current_user_id=company_user.id
        )
        log.info(f"Found {result.total} positions for company {company.slug}")
        return result
    except Exception as e:
        log.error(f"Error listing positions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/positions/{position_id}", response_model=JobPositionResponse)
@inject
def get_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionResponse:
    """Get a specific job position by ID"""
    try:
        position = controller.get_position_by_id(position_id)
        # Verify the position belongs to the company
        if position.company_id != company.id:
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


@router.post("/positions", response_model=JobPositionActionResponse)
@inject
def create_position(
    position_data: JobPositionCreate,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Create a new job position"""
    try:
        # Override company_id with the one from URL context
        # This ensures the position is created for the correct company
        position_data_dict = position_data.model_dump()
        position_data_dict['company_id'] = company.id
        updated_position_data = JobPositionCreate(**position_data_dict)

        return controller.create_position(updated_position_data)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error creating position: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/positions/{position_id}", response_model=JobPositionActionResponse)
@inject
def update_position(
    position_id: str,
    position_data: JobPositionUpdate,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Update an existing job position"""
    try:
        # Verify the position belongs to the company
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )
        return controller.update_position(position_id, position_data)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/positions/{position_id}", response_model=JobPositionActionResponse)
@inject
def delete_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Delete a job position"""
    try:
        # Verify the position belongs to the company
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )
        return controller.delete_position(position_id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/move-to-stage", response_model=dict)
@inject
def move_position_to_stage(
    position_id: str,
    request: MoveJobPositionToStageRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> dict:
    """Move a job position to a new stage with validation"""
    from src.company_bc.job_position.application.commands.move_job_position_to_stage import JobPositionValidationError

    try:
        # Verify the position belongs to the company
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        # Move the position to the new stage
        return controller.move_position_to_stage(
            position_id=position_id,
            stage_id=request.stage_id,
            comment=request.comment,
            user_id=company_user.id
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


# ==================== STATUS TRANSITION ENDPOINTS ====================

@router.post("/positions/{position_id}/request-approval", response_model=JobPositionActionResponse)
@inject
def request_approval(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Request approval for a job position (DRAFT -> PENDING_APPROVAL)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.request_approval(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error requesting approval for position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/approve", response_model=JobPositionActionResponse)
@inject
def approve_position(
    position_id: str,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Approve a job position (PENDING_APPROVAL -> APPROVED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.approve_position(
            position_id=position_id,
            approver_id=company_user.id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error approving position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/reject", response_model=JobPositionActionResponse)
@inject
def reject_position(
    position_id: str,
    request: RejectJobPositionRequest,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Reject a job position (PENDING_APPROVAL -> REJECTED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.reject_position(
            position_id=position_id,
            company_id=company.id,
            reason=request.reason
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error rejecting position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/publish", response_model=JobPositionActionResponse)
@inject
def publish_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Publish a job position (APPROVED/DRAFT -> PUBLISHED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.publish_position(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error publishing position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/hold", response_model=JobPositionActionResponse)
@inject
def hold_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Put a job position on hold (PUBLISHED -> ON_HOLD)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.hold_position(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error putting position {position_id} on hold: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/resume", response_model=JobPositionActionResponse)
@inject
def resume_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Resume a held job position (ON_HOLD -> PUBLISHED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.resume_position(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error resuming position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/close", response_model=JobPositionActionResponse)
@inject
def close_position(
    position_id: str,
    request: CloseJobPositionRequest,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Close a job position (PUBLISHED/ON_HOLD -> CLOSED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.close_position(
            position_id=position_id,
            company_id=company.id,
            closed_reason=request.reason
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error closing position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/archive", response_model=JobPositionActionResponse)
@inject
def archive_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Archive a job position (various -> ARCHIVED)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.archive_position(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error archiving position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/revert-to-draft", response_model=JobPositionActionResponse)
@inject
def revert_to_draft(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Revert a job position to draft (REJECTED/APPROVED/CLOSED -> DRAFT)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.revert_to_draft(
            position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error reverting position {position_id} to draft: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/clone", response_model=JobPositionActionResponse)
@inject
def clone_position(
    position_id: str,
    company: AdminCompanyContext,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> JobPositionActionResponse:
    """Clone a job position (creates new position in DRAFT)"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.clone_position(
            source_position_id=position_id,
            company_id=company.id
        )

        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error cloning position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/positions/{position_id}/screening-template", response_model=CreateInlineScreeningTemplateResponse)
@inject
def create_inline_screening_template(
    position_id: str,
    request: CreateInlineScreeningTemplateRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: JobPositionController = Depends(Provide[Container.job_position_controller]),
) -> CreateInlineScreeningTemplateResponse:
    """Create a screening template inline and link it to a job position"""
    try:
        position = controller.get_position_by_id(position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        result = controller.create_inline_screening_template(
            position_id=position_id,
            company_id=company.id,
            name=request.name,
            intro=request.intro,
            prompt=request.prompt,
            goal=request.goal,
            created_by=company_user.id
        )

        return CreateInlineScreeningTemplateResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error creating inline screening template for position {position_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== CANDIDATE MANAGEMENT ====================

@router.get("/candidates", response_model=List[CompanyCandidateResponse])
@inject
def list_company_candidates(
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> List[CompanyCandidateResponse]:
    """List all candidates for this company"""
    return controller.list_company_candidates_by_company(company.id)


@router.get("/candidates/{company_candidate_id}", response_model=CompanyCandidateResponse)
@inject
def get_company_candidate(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Get a company candidate by ID"""
    result = controller.get_company_candidate_by_id(company_candidate_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")

    # Verify the candidate belongs to this company
    if result.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidate does not belong to your company"
        )
    return result


@router.post("/candidates", response_model=CompanyCandidateResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_company_candidate(
    request: CreateCompanyCandidateRequest,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Create a new company candidate relationship"""
    try:
        # Override company_id with the one from URL context
        request_dict = request.model_dump()
        request_dict['company_id'] = company.id
        updated_request = CreateCompanyCandidateRequest(**request_dict)

        return controller.create_company_candidate(updated_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/candidates/{company_candidate_id}", response_model=CompanyCandidateResponse)
@inject
def update_company_candidate(
    company_candidate_id: str,
    request: UpdateCompanyCandidateRequest,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Update company candidate information"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.update_company_candidate(company_candidate_id, request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/candidates/{company_candidate_id}/confirm", response_model=CompanyCandidateResponse)
@inject
def confirm_company_candidate(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Confirm/accept a company candidate"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.confirm_company_candidate(company_candidate_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/candidates/{company_candidate_id}/reject", response_model=CompanyCandidateResponse)
@inject
def reject_company_candidate(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Reject/decline a company candidate"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.reject_company_candidate(company_candidate_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/candidates/{company_candidate_id}/archive", response_model=CompanyCandidateResponse)
@inject
def archive_company_candidate(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Archive a company candidate relationship"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.archive_company_candidate(company_candidate_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/candidates/{company_candidate_id}/assign-workflow", response_model=CompanyCandidateResponse)
@inject
def assign_workflow_to_candidate(
    company_candidate_id: str,
    request: AssignWorkflowRequest,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Assign a workflow to a company candidate"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.assign_workflow(company_candidate_id, request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/candidates/{company_candidate_id}/change-stage", response_model=CompanyCandidateResponse)
@inject
def change_candidate_stage(
    company_candidate_id: str,
    request: ChangeStageRequest,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Change the workflow stage of a company candidate"""
    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        return controller.change_stage(company_candidate_id, request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ==================== CANDIDATE REPORT GENERATION ====================

class GenerateReportRequest(BaseModel):
    """Request to generate a candidate report"""
    include_comments: bool = Field(True, description="Include comments in report")
    include_interviews: bool = Field(True, description="Include interviews in report")
    include_reviews: bool = Field(True, description="Include reviews in report")


class ReportSectionsResponse(BaseModel):
    """Report sections response"""
    summary: str
    strengths: List[str]
    areas_for_improvement: List[str]
    interview_insights: Optional[str] = None
    recommendation: str


class CandidateReportResponse(BaseModel):
    """Response containing the generated candidate report"""
    report_id: str
    company_candidate_id: str
    candidate_name: str
    generated_at: str
    report_markdown: str
    sections: ReportSectionsResponse


@router.post("/candidates/{company_candidate_id}/report", response_model=CandidateReportResponse)
@inject
def generate_candidate_report(
    company_candidate_id: str,
    request: GenerateReportRequest,
    company: AdminCompanyContext,
    controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller]),
    query_bus: QueryBus = Depends(Provide[Container.query_bus])
) -> CandidateReportResponse:
    """
    Generate an AI-powered report for a candidate.

    The report analyzes comments, interviews, and reviews to provide:
    - Executive summary
    - Strengths analysis
    - Areas for improvement
    - Interview insights
    - Hiring recommendation
    """
    from src.company_bc.company_candidate.application.queries.generate_candidate_report_query import (
        GenerateCandidateReportQuery
    )

    try:
        # Verify the candidate belongs to this company
        existing = controller.get_company_candidate_by_id(company_candidate_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
        if existing.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidate does not belong to your company"
            )

        query = GenerateCandidateReportQuery(
            company_candidate_id=company_candidate_id,
            include_comments=request.include_comments,
            include_interviews=request.include_interviews,
            include_reviews=request.include_reviews
        )

        result: Any = query_bus.query(query)

        return CandidateReportResponse(
            report_id=result.report_id,
            company_candidate_id=result.company_candidate_id,
            candidate_name=result.candidate_name,
            generated_at=result.generated_at,
            report_markdown=result.report_markdown,
            sections=ReportSectionsResponse(**result.sections)
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


# ==================== CANDIDATE APPLICATION MANAGEMENT ====================

class AssignCandidateToPositionRequest(BaseModel):
    """Request to assign a candidate to a position"""
    candidate_id: str
    job_position_id: str


@router.post("/applications", status_code=status.HTTP_201_CREATED)
@inject
def assign_candidate_to_position(
    request: AssignCandidateToPositionRequest,
    company: AdminCompanyContext,
    controller: ApplicationController = Depends(Provide[Container.application_controller]),
    position_controller: JobPositionController = Depends(Provide[Container.job_position_controller])
) -> dict:
    """
    Company assigns a candidate to a position by creating a candidate_application.
    This is for company-initiated assignments, not candidate-initiated applications.
    """
    try:
        # Verify the position belongs to this company
        position = position_controller.get_position_by_id(request.job_position_id)
        if position.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Position does not belong to your company"
            )

        application_id = controller.create_application(
            candidate_id=request.candidate_id,
            job_position_id=request.job_position_id,
            cover_letter=None  # Company assignment doesn't have cover letter
        )

        return {
            "application_id": application_id,
            "message": "Candidate assigned to position successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to assign candidate: {str(e)}"
        )


@router.get("/applications/{application_id}/can-process", status_code=status.HTTP_200_OK)
@inject
def check_user_can_process_application(
    application_id: str,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: ApplicationController = Depends(Provide[Container.application_controller])
) -> dict:
    """
    Check if the current user has permission to process an application at its current stage.
    Returns a boolean indicating whether the user can process the application.
    """
    try:
        can_process = controller.can_user_process_application(
            user_id=company_user.user_id,
            application_id=application_id,
            company_id=company.id
        )

        return {
            "can_process": can_process,
            "application_id": application_id,
            "user_id": company_user.user_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check permissions: {str(e)}"
        )


# ==================== INTERVIEW MANAGEMENT ====================

@router.get("/interviews", response_model=InterviewListResource)
@inject
def list_interviews(
    company: AdminCompanyContext,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
    candidate_id: Optional[str] = Query(None, description="Filter by candidate ID"),
    job_position_id: Optional[str] = Query(None, description="Filter by job position ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    from_date: Optional[datetime] = Query(None, description="Filter from date"),
    to_date: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(50, ge=1, le=100, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
) -> InterviewListResource:
    """List interviews for this company"""
    return controller.list_interviews(
        company_id=company.id,
        candidate_id=candidate_id,
        job_position_id=job_position_id,
        status=status,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset
    )


@router.get("/interviews/statistics", response_model=InterviewStatsResource)
@inject
def get_interview_stats(
    company: AdminCompanyContext,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewStatsResource:
    """Get interview statistics for this company"""
    return controller.get_interview_statistics(company_id=company.id)


@router.get("/interviews/{interview_id}", response_model=InterviewResource)
@inject
def get_interview(
    interview_id: str,
    company: AdminCompanyContext,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewResource:
    """Get a specific interview by ID"""
    interview = controller.get_interview_by_id(interview_id)
    # TODO: Verify interview belongs to company via candidate/position
    return interview


@router.get("/interviews/{interview_id}/view", response_model=InterviewFullResource)
@inject
def get_interview_view(
    interview_id: str,
    company: AdminCompanyContext,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewFullResource:
    """Get a specific interview with full details"""
    return controller.get_interview_view(interview_id)


@router.post("/interviews", response_model=InterviewActionResource, status_code=status.HTTP_201_CREATED)
@inject
def create_interview(
    interview_data: InterviewCreateRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewActionResource:
    """Create a new interview"""
    return controller.create_interview(
        candidate_id=interview_data.candidate_id,
        required_roles=interview_data.required_roles,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        process_type=interview_data.process_type,
        job_position_id=interview_data.job_position_id,
        stage_id=interview_data.workflow_stage_id,
        application_id=interview_data.application_id,
        interview_template_id=interview_data.interview_template_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
        interviewers=interview_data.interviewers,
        created_by=company_user.id
    )


@router.put("/interviews/{interview_id}", response_model=InterviewActionResource)
@inject
def update_interview(
    interview_id: str,
    interview_data: InterviewUpdateRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewActionResource:
    """Update an existing interview"""
    return controller.update_interview(
        interview_id=interview_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
        process_type=interview_data.process_type,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        status=interview_data.status,
        required_roles=interview_data.required_roles,
        interviewers=interview_data.interviewers,
        interviewer_notes=interview_data.interviewer_notes,
        feedback=interview_data.feedback,
        score=interview_data.score,
        updated_by=company_user.id
    )


@router.post("/interviews/{interview_id}/start", response_model=InterviewActionResource)
@inject
def start_interview(
    interview_id: str,
    start_data: StartInterviewRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewActionResource:
    """Start an interview"""
    return controller.start_interview(
        interview_id=interview_id,
        started_by=start_data.started_by or company_user.id
    )


@router.post("/interviews/{interview_id}/finish", response_model=InterviewActionResource)
@inject
def finish_interview(
    interview_id: str,
    finish_data: FinishInterviewRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewController = Depends(Provide[Container.interview_controller]),
) -> InterviewActionResource:
    """Finish an interview"""
    return controller.finish_interview(
        interview_id=interview_id,
        finished_by=finish_data.finished_by or company_user.id
    )


# ==================== INTERVIEW TEMPLATE MANAGEMENT ====================

@router.get("/interview-templates", response_model=List[InterviewTemplateResponse])
@inject
def list_interview_templates(
    company: AdminCompanyContext,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
    search_term: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: Optional[int] = Query(None),
    page_size: Optional[int] = Query(None)
) -> List[InterviewTemplateResponse]:
    """List interview templates for this company"""
    return controller.list_interview_templates(
        search_term=search_term,
        type=type,
        status=status,
        page=page,
        page_size=page_size,
        company_id=company.id
    )


@router.post("/interview-templates", response_model=InterviewTemplateResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_interview_template(
    template_data: InterviewTemplateCreate,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
) -> InterviewTemplateResponse:
    """Create a new interview template"""
    return controller.create_interview_template(
        template_data=template_data,
        current_admin_id=company_user.id,
        company_id=company.id
    )


@router.get("/interview-templates/{template_id}", response_model=InterviewTemplateResponse)
@inject
def get_interview_template(
    template_id: str,
    company: AdminCompanyContext,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
) -> InterviewTemplateResponse:
    """Get a specific interview template by ID"""
    template = controller.get_interview_template(template_id=template_id)

    # Verify template belongs to the company
    if template.company_id and template.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview template not found")

    return template


@router.put("/interview-templates/{template_id}", response_model=InterviewTemplateResponse)
@inject
def update_interview_template(
    template_id: str,
    template_data: InterviewTemplateCreate,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
) -> InterviewTemplateResponse:
    """Update an interview template"""
    # Verify template belongs to the company
    existing = controller.get_interview_template(template_id=template_id)
    if existing.company_id and existing.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview template not found")

    return controller.update_interview_template(
        template_id=template_id,
        template_data=template_data,
        current_admin_id=company_user.id,
        company_id=company.id
    )


@router.delete("/interview-templates/{template_id}")
@inject
def delete_interview_template(
    template_id: str,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
    delete_reason: Optional[str] = Query(None),
    force_delete: bool = Query(False)
) -> dict:
    """Delete an interview template"""
    # Verify template belongs to the company
    existing = controller.get_interview_template(template_id=template_id)
    if existing.company_id and existing.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview template not found")

    return controller.delete_interview_template(
        template_id=template_id,
        current_admin_id=company_user.id,
        delete_reason=delete_reason,
        force_delete=force_delete
    )


@router.post("/interview-templates/{template_id}/enable")
@inject
def enable_interview_template(
    template_id: str,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
    enable_reason: Optional[str] = None
) -> dict:
    """Enable an interview template"""
    existing = controller.get_interview_template(template_id=template_id)
    if existing.company_id and existing.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview template not found")

    return controller.enable_interview_template(
        template_id=template_id,
        current_admin_id=company_user.id,
        enable_reason=enable_reason
    )


@router.post("/interview-templates/{template_id}/disable")
@inject
def disable_interview_template(
    template_id: str,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: InterviewTemplateController = Depends(Provide[Container.interview_template_controller]),
    disable_reason: Optional[str] = None,
    force_disable: bool = False
) -> dict:
    """Disable an interview template"""
    existing = controller.get_interview_template(template_id=template_id)
    if existing.company_id and existing.company_id != company.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview template not found")

    return controller.disable_interview_template(
        template_id=template_id,
        current_admin_id=company_user.id,
        disable_reason=disable_reason,
        force_disable=force_disable
    )


# ==================== WORKFLOW MANAGEMENT ====================

@router.get("/workflows", response_model=List[WorkflowResponse])
@inject
def list_workflows(
    company: AdminCompanyContext,
    workflow_type: Optional[str] = Query(None, description="Filter by workflow type (CA, PO, CO)"),
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> List[WorkflowResponse]:
    """List all workflows for this company"""
    return controller.list_workflows_by_company(company.id, workflow_type)


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
@inject
def get_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Get a workflow by ID"""
    result = controller.get_workflow_by_id(workflow_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    # TODO: Verify workflow belongs to company
    return result


@router.post("/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_workflow(
    request: CreateWorkflowRequest,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Create a new workflow"""
    try:
        # Override company_id with the one from URL context
        request_dict = request.model_dump()
        request_dict['company_id'] = company.id
        updated_request = CreateWorkflowRequest(**request_dict)
        return controller.create_workflow(updated_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
@inject
def update_workflow(
    workflow_id: str,
    request: UpdateWorkflowRequest,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Update workflow information"""
    try:
        return controller.update_workflow(workflow_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/workflows/{workflow_id}/activate", response_model=WorkflowResponse)
@inject
def activate_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Activate a workflow"""
    try:
        return controller.activate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/workflows/{workflow_id}/deactivate", response_model=WorkflowResponse)
@inject
def deactivate_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Deactivate a workflow"""
    try:
        return controller.deactivate_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/workflows/{workflow_id}/archive", response_model=WorkflowResponse)
@inject
def archive_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Archive a workflow"""
    try:
        return controller.archive_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/workflows/{workflow_id}/set-default", response_model=WorkflowResponse)
@inject
def set_default_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> WorkflowResponse:
    """Set a workflow as default for this company"""
    try:
        return controller.set_as_default_workflow(workflow_id, company.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/workflows/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_workflow(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowController = Depends(Provide[Container.candidate_application_workflow_controller])
) -> None:
    """Delete a workflow"""
    try:
        controller.delete_workflow(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ==================== WORKFLOW STAGE MANAGEMENT ====================

@router.get("/workflows/{workflow_id}/stages", response_model=List[WorkflowStageResponse])
@inject
def list_workflow_stages(
    workflow_id: str,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """List all stages for a workflow"""
    return controller.list_stages_by_workflow(workflow_id)


@router.get("/workflow-stages/{stage_id}", response_model=WorkflowStageResponse)
@inject
def get_workflow_stage(
    stage_id: str,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Get a workflow stage by ID"""
    result = controller.get_stage_by_id(stage_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stage not found")
    return result


@router.post("/workflow-stages", response_model=WorkflowStageResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_workflow_stage(
    request: CreateStageRequest,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Create a new workflow stage"""
    try:
        return controller.create_stage(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/workflow-stages/{stage_id}", response_model=WorkflowStageResponse)
@inject
def update_workflow_stage(
    stage_id: str,
    request: UpdateStageRequest,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Update a workflow stage"""
    try:
        return controller.update_stage(stage_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/workflow-stages/{stage_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_workflow_stage(
    stage_id: str,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> None:
    """Delete a workflow stage"""
    try:
        controller.delete_stage(stage_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/workflows/{workflow_id}/stages/reorder", response_model=List[WorkflowStageResponse])
@inject
def reorder_workflow_stages(
    workflow_id: str,
    request: ReorderStagesRequest,
    company: AdminCompanyContext,
    controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """Reorder stages in a workflow"""
    try:
        return controller.reorder_stages(workflow_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ==================== CANDIDATE COMMENTS ====================

@router.get("/candidates/{company_candidate_id}/comments", response_model=List[CandidateCommentResponse])
@inject
def list_candidate_comments(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> List[CandidateCommentResponse]:
    """Get all comments for a candidate"""
    return controller.list_comments_by_company_candidate(company_candidate_id)


@router.post("/candidates/{company_candidate_id}/comments", response_model=CandidateCommentResponse,
             status_code=status.HTTP_201_CREATED)
@inject
def create_candidate_comment(
    company_candidate_id: str,
    request: CreateCandidateCommentRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Create a new comment for a candidate"""
    return controller.create_comment(company_candidate_id, request, company_user.id)


@router.get("/comments/{comment_id}", response_model=CandidateCommentResponse)
@inject
def get_comment(
    comment_id: str,
    company: AdminCompanyContext,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Get a comment by ID"""
    result = controller.get_comment_by_id(comment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return result


@router.put("/comments/{comment_id}", response_model=CandidateCommentResponse)
@inject
def update_comment(
    comment_id: str,
    request: UpdateCandidateCommentRequest,
    company: AdminCompanyContext,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Update a comment"""
    result = controller.update_comment(comment_id, request)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return result


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_comment(
    comment_id: str,
    company: AdminCompanyContext,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> None:
    """Delete a comment"""
    controller.delete_comment(comment_id)


# ==================== CANDIDATE REVIEWS ====================

@router.get("/candidates/{company_candidate_id}/reviews", response_model=List[ReviewResponse])
@inject
def list_candidate_reviews(
    company_candidate_id: str,
    company: AdminCompanyContext,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> List[ReviewResponse]:
    """Get all reviews for a candidate"""
    return controller.list_reviews_by_company_candidate(company_candidate_id)


@router.post("/candidates/{company_candidate_id}/reviews", response_model=ReviewResponse,
             status_code=status.HTTP_201_CREATED)
@inject
def create_candidate_review(
    company_candidate_id: str,
    request: CreateReviewRequest,
    company: AdminCompanyContext,
    company_user: CurrentCompanyUser,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Create a new review for a candidate"""
    return controller.create_review(company_candidate_id, request, company_user.id)


@router.get("/reviews/{review_id}", response_model=ReviewResponse)
@inject
def get_review(
    review_id: str,
    company: AdminCompanyContext,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Get a review by ID"""
    result = controller.get_review_by_id(review_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return result


@router.put("/reviews/{review_id}", response_model=ReviewResponse)
@inject
def update_review(
    review_id: str,
    request: UpdateReviewRequest,
    company: AdminCompanyContext,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> ReviewResponse:
    """Update a review"""
    return controller.update_review(review_id, request)


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_review(
    review_id: str,
    company: AdminCompanyContext,
    controller: ReviewController = Depends(Provide[Container.review_controller])
) -> None:
    """Delete a review"""
    controller.delete_review(review_id)
