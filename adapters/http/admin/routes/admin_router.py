"""
Admin router minimal - Solo interview templates por ahora
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from adapters.http.admin.controllers.admin_candidate_controller import AdminCandidateController
from adapters.http.admin.controllers.company_controller import CompanyController
from adapters.http.admin.controllers.enum_controller import EnumController, EnumMetadataResponse
from adapters.http.admin.controllers.interview_controller import InterviewController
from adapters.http.admin.controllers.inverview_template_controller import InterviewTemplateController
from adapters.http.admin.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.admin.controllers.job_position_controller import JobPositionController
from adapters.http.admin.controllers.job_position_workflow_controller import JobPositionWorkflowController
# Company schemas
from adapters.http.admin.schemas.company import (
    CompanyResponse, CompanyCreate, CompanyUpdate, CompanyListResponse,
    CompanyStatsResponse, CompanyActionResponse, CompanyStatusUpdate
)
# Interview management schemas
from adapters.http.admin.schemas.interview_management import (
    InterviewCreateRequest, InterviewUpdateRequest, InterviewManagementResponse,
    InterviewListResponse, InterviewStatsResponse, InterviewActionResponse,
    InterviewScoreSummaryResponse, StartInterviewRequest, FinishInterviewRequest
)
# Interview template schemas
from adapters.http.admin.schemas.interview_template import (
    InterviewTemplateResponse, InterviewTemplateCreate,
    InterviewTemplateSectionCreate, InterviewTemplateSectionUpdate,
    InterviewTemplateQuestionCreate, InterviewTemplateQuestionUpdate
)
# Job position schemas
from adapters.http.admin.schemas.job_position import (
    JobPositionResponse, JobPositionCreate, JobPositionUpdate, JobPositionListResponse,
    JobPositionStatsResponse, JobPositionActionResponse
)
from adapters.http.admin.schemas.job_position_activity import (
    JobPositionActivityListResponse
)
from adapters.http.admin.schemas.job_position_comment import (
    CreateJobPositionCommentRequest, UpdateJobPositionCommentRequest,
    JobPositionCommentResponse, JobPositionCommentListResponse
)
from adapters.http.admin.schemas.job_position_workflow import (
    JobPositionWorkflowCreate, JobPositionWorkflowUpdate, JobPositionWorkflowResponse,
    MoveJobPositionToStageRequest, UpdateJobPositionCustomFieldsRequest
)
from adapters.http.shared.schemas.token import Token
from adapters.http.shared.schemas.user import UserResponse
from core.container import Container
from src.company.application.dtos import CompanyUserDto
from src.company.domain import CompanyId
from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.shared.application.query_bus import QueryBus
from src.user.application.queries.authenticate_user_query import AuthenticateUserQuery
from src.user.application.queries.dtos.auth_dto import CurrentUserDto, AuthenticatedUserDto
from src.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

# OAuth2 scheme for admin token extraction
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/auth/login")


@dataclass
class CurrentAdminUser:
    id: str
    email: str


# Real admin authentication using JWT token


@inject
def get_current_admin_user(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        token: str = Security(admin_oauth2_scheme),
) -> CurrentAdminUser:
    """Get current admin user from JWT token"""
    try:
        query = GetCurrentUserFromTokenQuery(token=token)
        user_dto: CurrentUserDto = query_bus.query(query)

        if not user_dto:
            raise HTTPException(status_code=401, detail="Invalid token")

        # TODO: Add admin role validation here when roles are implemented
        # For now, any valid authenticated user can access admin endpoints

        return CurrentAdminUser(
            id=str(user_dto.user_id),
            email=user_dto.email
        )

    except Exception as e:
        logger.error(f"Error getting current admin user: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


# Interview Template Management - Solo endpoints básicos


@router.get("/interview-templates", response_model=List[InterviewTemplateResponse])
@inject
def list_interview_templates(
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        search_term: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        job_category: Optional[str] = None,
        section: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None
) -> List[InterviewTemplateResponse]:
    """List all interview templates with filtering options"""
    return controller.list_interview_templates(
        search_term=search_term,
        type=type,
        status=status,
        job_category=job_category,
        section=section,
        page=page,
        page_size=page_size
    )


@router.post("/interview-templates", response_model=InterviewTemplateResponse)
@inject
def create_interview_template(
        template_data: InterviewTemplateCreate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewTemplateResponse:
    """Create a new interview template"""
    return controller.create_interview_template(template_data=template_data, current_admin_id=current_admin.id)


@router.get("/interview-templates/{template_id}", response_model=InterviewTemplateResponse)
@inject
def get_interview_template(
        template_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
) -> InterviewTemplateResponse:
    """Get a specific interview template by ID"""
    return controller.get_interview_template(template_id=template_id)


@router.put("/interview-templates/{template_id}", response_model=InterviewTemplateResponse)
@inject
def update_interview_template(
        template_id: str,
        template_data: InterviewTemplateCreate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewTemplateResponse:
    """Update an existing interview template"""
    template = controller.update_interview_template(template_id=template_id, template_data=template_data,
                                                    current_admin_id=current_admin.id)
    return template


@router.post("/interview-templates/{template_id}/enable")
@inject
def enable_interview_template(
        template_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        enable_reason: Optional[str] = None
) -> dict:
    return controller.enable_interview_template(
        template_id=template_id,
        current_admin_id=current_admin.id,
        enable_reason=enable_reason
    )


@router.post("/interview-templates/{template_id}/disable")
@inject
def disable_interview_template(
        template_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        disable_reason: Optional[str] = None,
        force_disable: bool = False
) -> dict:
    return controller.disable_interview_template(
        template_id=template_id,
        current_admin_id=current_admin.id,
        disable_reason=disable_reason,
        force_disable=force_disable
    )


@router.delete("/interview-templates/{template_id}")
@inject
def delete_interview_template(
        template_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        delete_reason: Optional[str] = Query(None),
        force_delete: bool = Query(False)
) -> dict:
    return controller.delete_interview_template(
        template_id=template_id,
        current_admin_id=current_admin.id,
        delete_reason=delete_reason,
        force_delete=force_delete
    )


# Interview Template Section Management


@router.post("/interview-template-sections")
@inject
def create_interview_template_section(
        section_data: InterviewTemplateSectionCreate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.create_interview_template_section(
        section_data=section_data,
        current_admin_id=current_admin.id
    )


@router.put("/interview-template-sections/{section_id}")
@inject
def update_interview_template_section(
        section_id: str,
        section_data: InterviewTemplateSectionUpdate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.update_interview_template_section(
        section_id=section_id,
        section_data=section_data,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-sections/{section_id}/enable")
@inject
def enable_interview_template_section(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.enable_interview_template_section(
        section_id=section_id,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-sections/{section_id}/disable")
@inject
def disable_interview_template_section(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.disable_interview_template_section(
        section_id=section_id,
        current_admin_id=current_admin.id
    )


@router.delete("/interview-template-sections/{section_id}")
@inject
def delete_interview_template_section(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.delete_interview_template_section(
        section_id=section_id,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-sections/{section_id}/move-up")
@inject
def move_section_up(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.move_section_up(
        section_id=section_id,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-sections/{section_id}/move-down")
@inject
def move_section_down(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.move_section_down(
        section_id=section_id,
        current_admin_id=current_admin.id
    )


# Interview Template Question Management


@router.get("/interview-template-sections/{section_id}/questions")
@inject
def get_questions_by_section(
        section_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
) -> list:
    return controller.get_questions_by_section(section_id=section_id)


@router.post("/interview-template-questions")
@inject
def create_interview_template_question(
        question_data: InterviewTemplateQuestionCreate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
) -> dict:
    return controller.create_interview_template_question(question_data=question_data)


@router.put("/interview-template-questions/{question_id}")
@inject
def update_interview_template_question(
        question_id: str,
        question_data: InterviewTemplateQuestionUpdate,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.update_interview_template_question(
        question_id=question_id,
        question_data=question_data,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-questions/{question_id}/enable")
@inject
def enable_interview_template_question(
        question_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.enable_interview_template_question(
        question_id=question_id,
        current_admin_id=current_admin.id
    )


@router.post("/interview-template-questions/{question_id}/disable")
@inject
def disable_interview_template_question(
        question_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.disable_interview_template_question(
        question_id=question_id,
        current_admin_id=current_admin.id
    )


@router.delete("/interview-template-questions/{question_id}")
@inject
def delete_interview_template_question(
        question_id: str,
        controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    return controller.delete_interview_template_question(
        question_id=question_id,
        current_admin_id=current_admin.id
    )


# Dashboard endpoint


@router.get("/dashboard")
def get_dashboard(
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    """Get admin dashboard - simplified for Interview Templates focus"""
    return {
        "user_id": current_admin.id,
        "interview_templates_count": 0,  # TODO: Get real count when needed
        "generated_at": datetime.utcnow().isoformat()
    }


# Company Management Endpoints


@router.get("/companies", response_model=CompanyListResponse)
@inject
def list_companies(
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        search_term: Optional[str] = Query(None, description="Search in company names"),
        status: Optional[str] = Query(None, description="Filter by status"),
        page: Optional[int] = Query(1, ge=1, description="Page number"),
        page_size: Optional[int] = Query(10, ge=1, le=100, description="Items per page")
) -> CompanyListResponse:
    """List companies with filtering options"""
    return controller.list_companies(
        search_term=search_term,
        status=status,
        page=page,
        page_size=page_size
    )


@router.get("/companies/stats", response_model=CompanyStatsResponse)
@inject
def get_companies_stats(
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyStatsResponse:
    """Get company statistics"""
    return controller.get_company_stats()


@router.get("/companies/{company_id}", response_model=CompanyResponse)
@inject
def get_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
) -> CompanyResponse:
    """Get a specific company by ID"""
    return controller.get_company_by_id(CompanyId.from_string(company_id))


@router.post("/companies", response_model=CompanyResponse)
@inject
async def create_company(
        request: Request,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyResponse:
    """Create a new company"""
    # Debug: Get raw body
    body = await request.body()
    logger.info(f"Raw body: {body.decode('utf-8') if body else 'empty'}")

    # Try to parse JSON manually
    import json
    try:
        json_data = json.loads(body)
        logger.info(f"Parsed JSON: {json_data}")

        # user_id is now optional, no need to auto-create users

        # Create CompanyCreate object manually
        company_data = CompanyCreate(**json_data)
        logger.info(f"Created CompanyCreate object: {company_data}")

        # Use real authenticated admin ID
        return controller.create_company(company_data=company_data, current_admin_id=current_admin.id)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/companies/{company_id}", response_model=CompanyResponse)
@inject
def update_company(
        company_id: str,
        company_data: CompanyUpdate,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyResponse:
    """Update an existing company"""
    return controller.update_company(
        company_id=CompanyId(company_id),
        company_data=company_data,
        current_admin_id=current_admin.id
    )


@router.post("/companies/{company_id}/approve", response_model=CompanyActionResponse)
@inject
def approve_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyActionResponse:
    """Approve a pending company"""
    return controller.approve_company(company_id=CompanyId.from_string(company_id), current_admin_id=current_admin.id)


@router.post("/companies/{company_id}/reject", response_model=CompanyActionResponse)
@inject
def reject_company(
        company_id: str,
        status_update: CompanyStatusUpdate,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyActionResponse:
    """Reject a pending company"""
    return controller.reject_company(
        company_id=CompanyId.from_string(company_id),
        reason=status_update.reason
    )


@router.post("/companies/{company_id}/activate", response_model=CompanyActionResponse)
@inject
def activate_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyActionResponse:
    """Activate an inactive company"""
    return controller.activate_company(company_id=CompanyId.from_string(company_id))


@router.post("/companies/{company_id}/deactivate", response_model=CompanyActionResponse)
@inject
def deactivate_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyActionResponse:
    """Deactivate an active company"""
    return controller.deactivate_company(company_id=CompanyId.from_string(company_id),
                                         current_admin_id=current_admin.id)


@router.delete("/companies/{company_id}", response_model=CompanyActionResponse)
@inject
def delete_company(
        company_id: str,
        controller: Annotated[CompanyController, Depends(Provide[Container.company_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> CompanyActionResponse:
    """Delete a company"""
    return controller.delete_company(company_id=CompanyId.from_string(company_id), current_admin_id=current_admin.id)


# Job Position Management Endpoints
@router.get("/positions", response_model=JobPositionListResponse)
@inject
def list_positions(
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_id: Optional[str] = Query(None, description="Filter by company ID"),
        search_term: Optional[str] = Query(None, description="Search in position titles"),
        department: Optional[str] = Query(None, description="Filter by department"),
        location: Optional[str] = Query(None, description="Filter by location"),
        employment_type: Optional[str] = Query(None, description="Filter by employment type"),
        experience_level: Optional[str] = Query(None, description="Filter by experience level"),
        is_remote: Optional[bool] = Query(None, description="Filter by remote work"),
        is_active: Optional[bool] = Query(None, description="Filter by active status"),
        page: Optional[int] = Query(1, ge=1, description="Page number"),
        page_size: Optional[int] = Query(10, ge=1, le=100, description="Items per page")
) -> JobPositionListResponse:
    """List job positions with filtering options"""
    # Get company_user_id for the current user (if company_id provided)
    company_user_id = None
    if company_id:
        from src.company.application.queries.get_company_user_by_company_and_user import \
            GetCompanyUserByCompanyAndUserQuery
        company_user_query = GetCompanyUserByCompanyAndUserQuery(
            company_id=company_id,
            user_id=current_admin.id
        )
        company_user_dto: Optional[CompanyUserDto] = query_bus.query(company_user_query)
        if company_user_dto:
            company_user_id = company_user_dto.id

    return controller.list_positions(
        company_id=company_id,
        search_term=search_term,
        department=department,
        location=location,
        employment_type=employment_type,
        experience_level=experience_level,
        is_remote=is_remote,
        is_active=is_active,
        page=page,
        page_size=page_size,
        current_user_id=company_user_id
    )


@router.get("/positions/stats", response_model=JobPositionStatsResponse)
@inject
def get_positions_stats(
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
) -> JobPositionStatsResponse:
    """Get job position statistics"""
    return controller.get_position_stats()


@router.get("/positions/{position_id}", response_model=JobPositionResponse)
@inject
def get_position(
        position_id: str,
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
) -> JobPositionResponse:
    """Get a specific job position by ID"""
    return controller.get_position_by_id(position_id)


@router.post("/positions", response_model=JobPositionActionResponse)
@inject
def create_position(
        position_data: JobPositionCreate,
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> JobPositionActionResponse:
    """Create a new job position"""
    return controller.create_position(position_data)


@router.put("/positions/{position_id}", response_model=JobPositionActionResponse)
@inject
def update_position(
        position_id: str,
        position_data: JobPositionUpdate,
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> JobPositionActionResponse:
    """Update an existing job position"""
    return controller.update_position(position_id, position_data)


# Status management endpoints (activate, pause, resume, close, archive) have been removed.
# Use workflow endpoints instead: /workflows/{workflow_id}/positions/{position_id}/move-to-stage


@router.delete("/positions/{position_id}", response_model=JobPositionActionResponse)
@inject
def delete_position(
        position_id: str,
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> JobPositionActionResponse:
    """Delete a job position"""
    return controller.delete_position(position_id)


# ====================================
# JOB POSITION WORKFLOW ENDPOINTS
# ====================================

@router.post("/workflows", response_model=JobPositionWorkflowResponse)
@inject
def create_workflow(
        workflow_data: JobPositionWorkflowCreate,
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> JobPositionWorkflowResponse:
    """Create a new job position workflow"""
    return controller.create_workflow(workflow_data)


@router.get("/workflows/{workflow_id}", response_model=JobPositionWorkflowResponse)
@inject
def get_workflow(
        workflow_id: str,
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
) -> JobPositionWorkflowResponse:
    """Get a job position workflow by ID"""
    return controller.get_workflow(workflow_id)


@router.put("/workflows/{workflow_id}", response_model=JobPositionWorkflowResponse)
@inject
def update_workflow(
        workflow_id: str,
        workflow_data: JobPositionWorkflowUpdate,
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> JobPositionWorkflowResponse:
    """Update a job position workflow"""
    return controller.update_workflow(workflow_id, workflow_data)


@router.get("/workflows", response_model=List[JobPositionWorkflowResponse])
@inject
def list_workflows(
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        company_id: str = Query(..., description="Company ID"),
) -> List[JobPositionWorkflowResponse]:
    """List job position workflows for a company"""
    return controller.list_workflows(company_id)


@router.post("/workflows/initialize", response_model=List[JobPositionWorkflowResponse])
@inject
def initialize_default_workflows(
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        company_id: str = Query(..., description="Company ID"),
) -> List[JobPositionWorkflowResponse]:
    """Initialize default job position workflows for a company"""
    return controller.initialize_default_workflows(company_id)


@router.post("/positions/{position_id}/move-to-stage", response_model=dict)
@inject
def move_position_to_stage(
        position_id: str,
        request: MoveJobPositionToStageRequest,
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    """Move a job position to a new stage with validation"""
    from src.job_position.application.commands.move_job_position_to_stage import JobPositionValidationError
    from fastapi import HTTPException

    try:
        return controller.move_position_to_stage(position_id, request)
    except JobPositionValidationError as e:
        # Return 400 with validation errors
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "validation_errors": e.validation_errors
            }
        )


@router.put("/positions/{position_id}/custom-fields", response_model=dict)
@inject
def update_position_custom_fields(
        position_id: str,
        request: UpdateJobPositionCustomFieldsRequest,
        controller: Annotated[
            JobPositionWorkflowController, Depends(Provide[Container.job_position_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    """Update custom fields values for a job position"""
    return controller.update_custom_fields(position_id, request)


# Job Position Comments & Activity Endpoints


@router.post("/positions/{position_id}/comments", status_code=status.HTTP_201_CREATED)
@inject
def create_job_position_comment(
        position_id: str,
        request: CreateJobPositionCommentRequest,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        job_position_controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> None:
    """Create a new comment for a job position"""
    # Get the job position to find the company_id
    from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.job_position.domain.value_objects import JobPositionId
    from src.company.application.queries.get_company_user_by_company_and_user import GetCompanyUserByCompanyAndUserQuery

    position_query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
    position_dto: Optional[JobPositionDto] = query_bus.query(position_query)

    if not position_dto:
        raise HTTPException(status_code=404, detail="Job position not found")

    # Get company_user_id for the current user
    company_user_query = GetCompanyUserByCompanyAndUserQuery(
        company_id=position_dto.company_id.value,
        user_id=current_admin.id
    )
    company_user_dto: Optional[CompanyUserDto] = query_bus.query(company_user_query)

    if not company_user_dto:
        raise HTTPException(status_code=403, detail="User not authorized for this company")

    controller.create_comment(position_id, request, company_user_dto.id)


@router.get("/positions/{position_id}/comments/all", response_model=list[JobPositionCommentResponse])
@inject
def list_all_job_position_comments(
        position_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        job_position_controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
) -> list[JobPositionCommentResponse]:
    """List ALL comments for a job position (no filtering, visibility applied)"""
    # Get company_user_id for the current user
    from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.job_position.domain.value_objects import JobPositionId
    from src.company.application.queries.get_company_user_by_company_and_user import GetCompanyUserByCompanyAndUserQuery

    position_query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
    position_dto: Optional[JobPositionDto] = query_bus.query(position_query)

    company_user_id = None
    if position_dto:
        company_user_query = GetCompanyUserByCompanyAndUserQuery(
            company_id=position_dto.company_id.value,
            user_id=current_admin.id
        )
        company_user_dto: Optional[CompanyUserDto] = query_bus.query(company_user_query)
        if company_user_dto:
            company_user_id = company_user_dto.id

    response = controller.list_all_comments(position_id, current_user_id=company_user_id)
    return response.comments


@router.get("/positions/{position_id}/comments", response_model=JobPositionCommentListResponse)
@inject
def list_job_position_comments(
        position_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        job_position_controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        stage_id: Optional[str] = Query(None, description="Filter by stage (null = global comments only)"),
        include_global: bool = Query(True, description="Include global comments"),
) -> JobPositionCommentListResponse:
    """List comments for a job position (with visibility filtering)"""
    # Get company_user_id for the current user
    from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.job_position.domain.value_objects import JobPositionId
    from src.company.application.queries.get_company_user_by_company_and_user import GetCompanyUserByCompanyAndUserQuery

    position_query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
    position_dto: Optional[JobPositionDto] = query_bus.query(position_query)

    company_user_id = None
    if position_dto:
        company_user_query = GetCompanyUserByCompanyAndUserQuery(
            company_id=position_dto.company_id.value,
            user_id=current_admin.id
        )
        company_user_dto: Optional[CompanyUserDto] = query_bus.query(company_user_query)
        if company_user_dto:
            company_user_id = company_user_dto.id

    return controller.list_comments(position_id, stage_id, include_global, current_user_id=company_user_id)


@router.put("/positions/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def update_job_position_comment(
        comment_id: str,
        request: UpdateJobPositionCommentRequest,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> None:
    """Update a job position comment"""
    controller.update_comment(comment_id, request)


@router.delete("/positions/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_job_position_comment(
        comment_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> None:
    """Delete a job position comment"""
    controller.delete_comment(comment_id)


@router.post("/positions/comments/{comment_id}/mark-reviewed", status_code=status.HTTP_204_NO_CONTENT)
@inject
def mark_comment_as_reviewed(
        comment_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> None:
    """Mark a comment as reviewed"""
    controller.mark_comment_as_reviewed(comment_id)


@router.post("/positions/comments/{comment_id}/mark-pending", status_code=status.HTTP_204_NO_CONTENT)
@inject
def mark_comment_as_pending(
        comment_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> None:
    """Mark a comment as pending"""
    controller.mark_comment_as_pending(comment_id)


@router.get("/positions/{position_id}/activities", response_model=JobPositionActivityListResponse)
@inject
def list_job_position_activities(
        position_id: str,
        controller: Annotated[
            JobPositionCommentController, Depends(Provide[Container.job_position_comment_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        limit: int = Query(50, ge=1, le=100, description="Maximum number of activities"),
) -> JobPositionActivityListResponse:
    """List activities for a job position"""
    return controller.list_activities(position_id, limit)


# Enum metadata endpoint
@router.get("/enums/metadata", response_model=EnumMetadataResponse)
def get_enum_metadata() -> EnumMetadataResponse:
    """Get all enum definitions for frontend consumption"""
    controller = EnumController()
    return controller.get_enum_metadata()


# Candidate Management Endpoints


@router.get("/candidates")
@inject
def list_candidates(
        controller: Annotated[AdminCandidateController, Depends(Provide[Container.admin_candidate_controller])],
        search_term: Optional[str] = Query(None, description="Search in candidate names or emails"),
        status: Optional[str] = Query(None, description="Filter by status"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        offset: int = Query(0, ge=0, description="Offset for pagination")
) -> dict:
    """List candidates with filtering and pagination"""
    return controller.list_candidates(
        search_term=search_term,
        status=status,
        limit=limit,
        offset=offset
    )


@router.get("/candidates/stats")
@inject
def get_candidates_stats(
        controller: Annotated[AdminCandidateController, Depends(Provide[Container.admin_candidate_controller])],
) -> dict:
    """Get candidate statistics"""
    return controller.get_candidates_stats()


@router.get("/candidates/{candidate_id}")
@inject
def get_candidate_details(
        candidate_id: str,
        controller: Annotated[AdminCandidateController, Depends(Provide[Container.admin_candidate_controller])],
) -> dict:
    """Get detailed candidate and user information"""
    return controller.get_candidate_with_user(candidate_id)


@router.post("/candidates/{candidate_id}/set-password")
@inject
def set_candidate_password(
        candidate_id: str,
        password_data: dict,
        controller: Annotated[AdminCandidateController, Depends(Provide[Container.admin_candidate_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    """Set password for a candidate's user account (creates user account if needed)"""

    new_password = password_data.get("password")
    if not new_password or len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    return controller.update_user_password(
        candidate_id=candidate_id,
        new_password=new_password,
        admin_id=current_admin.id
    )


@router.get("/interview", response_model=InterviewListResponse)
@inject
def list_interviews(
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        candidate_id: Optional[str] = Query(None, description="Filter by candidate ID"),
        job_position_id: Optional[str] = Query(None, description="Filter by job position ID"),
        interview_type: Optional[str] = Query(None, description="Filter by interview type"),
        status: Optional[str] = Query(None, description="Filter by status"),
        created_by: Optional[str] = Query(None, description="Filter by creator"),
        from_date: Optional[datetime] = Query(None, description="Filter from date"),
        to_date: Optional[datetime] = Query(None, description="Filter to date"),
        limit: int = Query(50, ge=1, le=100, description="Limit results"),
        offset: int = Query(0, ge=0, description="Offset for pagination")
) -> InterviewListResponse:
    """List interviews with optional filtering"""
    interviews = controller.list_interviews(
        candidate_id=candidate_id,
        job_position_id=job_position_id,
        interview_type=interview_type,
        status=status,
        created_by=created_by,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset
    )

    return InterviewListResponse(
        interviews=[InterviewManagementResponse.from_dto(interview) for interview in interviews],
        total=len(interviews),
        page=1,
        page_size=limit
    )


@router.get("/interview/stats", response_model=InterviewStatsResponse)
@inject
def get_interview_stats(
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
) -> InterviewStatsResponse:
    """Get interview statistics"""
    # This would need to be implemented in the controller
    return InterviewStatsResponse(
        total_interviews=0,
        scheduled_interviews=0,
        in_progress_interviews=0,
        completed_interviews=0,
        average_score=None,
        average_duration_minutes=None
    )


@router.get("/interview/{interview_id}", response_model=InterviewManagementResponse)
@inject
def get_interview(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
) -> InterviewManagementResponse:
    """Get a specific interview by ID"""
    interview = controller.get_interview_by_id(interview_id)
    return InterviewManagementResponse.from_dto(interview)


@router.post("/interview", response_model=InterviewActionResponse)
@inject
def create_interview(
        interview_data: InterviewCreateRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewActionResponse:
    """Create a new interview"""
    result = controller.create_interview(
        candidate_id=interview_data.candidate_id,
        interview_type=interview_data.interview_type,
        job_position_id=interview_data.job_position_id,
        application_id=interview_data.application_id,
        interview_template_id=interview_data.interview_template_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        interviewers=interview_data.interviewers,
        created_by=current_admin.id
    )

    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=None  # Could be returned from controller if needed
    )


@router.put("/interview/{interview_id}", response_model=InterviewActionResponse)
@inject
def update_interview(
        interview_id: str,
        interview_data: InterviewUpdateRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewActionResponse:
    """Update an existing interview"""
    # This would need to be implemented in the controller
    return InterviewActionResponse(
        message="Interview updated successfully",
        status="success",
        interview_id=interview_id
    )


@router.post("/interview/{interview_id}/start", response_model=InterviewActionResponse)
@inject
def start_interview(
        interview_id: str,
        start_data: StartInterviewRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewActionResponse:
    """Start an interview"""
    result = controller.start_interview(
        interview_id=interview_id,
        started_by=start_data.started_by or current_admin.id
    )

    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=interview_id
    )


@router.post("/interview/{interview_id}/finish", response_model=InterviewActionResponse)
@inject
def finish_interview(
        interview_id: str,
        finish_data: FinishInterviewRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> InterviewActionResponse:
    """Finish an interview"""
    result = controller.finish_interview(
        interview_id=interview_id,
        finished_by=finish_data.finished_by or current_admin.id
    )

    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=interview_id
    )


@router.get("/interview/candidate/{candidate_id}", response_model=List[InterviewManagementResponse])
@inject
def get_interviews_by_candidate(
        candidate_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        status: Optional[str] = Query(None, description="Filter by status"),
        interview_type: Optional[str] = Query(None, description="Filter by interview type")
) -> List[InterviewManagementResponse]:
    """Get interviews for a specific candidate"""
    interviews = controller.get_interviews_by_candidate(
        candidate_id=candidate_id,
    )

    return [InterviewManagementResponse.from_dto(interview) for interview in interviews]


@router.get("/interview/scheduled", response_model=List[InterviewManagementResponse])
@inject
def get_scheduled_interviews(
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        from_date: Optional[datetime] = Query(None, description="Filter from date"),
        to_date: Optional[datetime] = Query(None, description="Filter to date"),
        interviewer: Optional[str] = Query(None, description="Filter by interviewer name")
) -> List[InterviewManagementResponse]:
    """Get scheduled interviews"""
    interviews = controller.get_scheduled_interviews(
        from_date=from_date,
        to_date=to_date,
    )

    return [InterviewManagementResponse.from_dto(interview) for interview in interviews]


@router.get("/interview/{interview_id}/score-summary", response_model=InterviewScoreSummaryResponse)
@inject
def get_interview_score_summary(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
) -> InterviewScoreSummaryResponse:
    """Get interview score summary"""

    return InterviewScoreSummaryResponse(
        interview_id=interview_id,
        overall_score=None,
        total_questions=0,
        answered_questions=0,
        average_answer_score=None,
        completion_percentage=0.0
    )


# ====================================
# ADMIN AUTH ENDPOINTS
# ====================================

@router.post("/auth/login", response_model=Token)
@inject
def admin_login(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Authenticate admin user and return JWT token"""
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

        # TODO: Add admin role validation here
        # For now, any valid user can access admin (same as mock)

        return Token(
            access_token=auth_result.access_token,
            token_type=auth_result.token_type,
            expires_in=2880 * 60,  # 48 hours in seconds
            candidate_id=None  # Admin users don't have candidate_id
        )

    except Exception as e:
        logger.error(f"Admin authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/auth/me", response_model=UserResponse)
@inject
def get_current_admin_user_info(
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)]
) -> UserResponse:
    """Get current admin user info"""
    return UserResponse(
        id=current_admin.id,
        email=current_admin.email,
        is_active=True,  # Admin users are always active when authenticated
        subscription_tier="ADMIN"  # Admin tier
    )


# Endpoint básico de health check
@router.get("/health")
def health_check() -> dict[str, str]:
    """Basic health check for admin panel"""
    return {"status": "ok", "message": "Admin panel - Interview Templates, Companies, and Candidates"}
