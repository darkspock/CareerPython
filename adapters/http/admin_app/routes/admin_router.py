"""
Admin router minimal - Solo interview templates por ahora
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request, Security, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from adapters.http.admin_app.controllers.company_controller import CompanyController
from adapters.http.admin_app.controllers.enum_controller import EnumController, EnumMetadataResponse
from adapters.http.admin_app.controllers.inverview_template_controller import InterviewTemplateController
# JobPositionWorkflowController removed - use generic WorkflowController or JobPositionController instead
from adapters.http.admin_app.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.admin_app.controllers.job_position_controller import JobPositionController
# Company schemas
from adapters.http.admin_app.schemas.company import (
    CompanyResponse, CompanyCreate, CompanyUpdate, CompanyListResponse,
    CompanyStatsResponse, CompanyActionResponse, CompanyStatusUpdate
)
# Interview template schemas
from adapters.http.admin_app.schemas.interview_template import (
    InterviewTemplateResponse, InterviewTemplateCreate,
    InterviewTemplateSectionCreate, InterviewTemplateSectionUpdate,
    InterviewTemplateQuestionCreate, InterviewTemplateQuestionUpdate
)
# Job position schemas
from adapters.http.admin_app.schemas.job_position import (
    JobPositionResponse, JobPositionCreate, JobPositionUpdate, JobPositionListResponse,
    JobPositionStatsResponse, JobPositionActionResponse
)
from adapters.http.admin_app.schemas.job_position_activity import (
    JobPositionActivityListResponse
)
from adapters.http.admin_app.schemas.job_position_comment import (
    CreateJobPositionCommentRequest, UpdateJobPositionCommentRequest,
    JobPositionCommentResponse, JobPositionCommentListResponse
)
from adapters.http.admin_app.schemas.job_position_workflow import (
    MoveJobPositionToStageRequest, UpdateJobPositionCustomFieldsRequest
)
from adapters.http.auth.schemas.token import Token
from adapters.http.auth.schemas.user import UserResponse
from adapters.http.shared.workflow.controllers import WorkflowController
from adapters.http.shared.workflow.schemas import WorkflowResponse
from adapters.http.shared.workflow.schemas.update_workflow_request import UpdateWorkflowRequest
from core.containers import Container
from src.auth_bc.user.application import AuthenticateUserQuery
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto, AuthenticatedUserDto
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery
from src.company_bc.company.application.dtos import CompanyUserDto
from src.company_bc.company.domain import CompanyId
from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

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
        page: Optional[int] = None,
        page_size: Optional[int] = None
) -> List[InterviewTemplateResponse]:
    """List all interview templates with filtering options"""
    return controller.list_interview_templates(
        search_term=search_term,
        type=type,
        status=status,
        job_category=job_category,
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
        from src.company_bc.company.application.queries.get_company_user_by_company_and_user import \
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


# Position CRUD operations (create, update, delete) are handled by company_position_router
# at /api/company/positions. Use those endpoints instead.


# ====================================
# JOB POSITION WORKFLOW ENDPOINTS
# ====================================
# Note: Workflow CRUD operations are now handled by the generic workflow system
# at /api/company-workflows. These endpoints are kept for backward compatibility
# but should be migrated to use the generic workflow endpoints.

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
@inject
def get_workflow(
        workflow_id: str,
        controller: Annotated[
            WorkflowController, Depends(Provide[Container.candidate_application_workflow_controller])],
) -> WorkflowResponse:
    """Get a workflow by ID (backward compatibility endpoint)"""
    result = controller.get_workflow_by_id(workflow_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    # Ensure stages is always a list (not None) for frontend compatibility
    if result.stages is None:
        result.stages = []

    # Transform stages to match frontend expected format
    # Frontend expects: icon, background_color, text_color, status_mapping, field_visibility, etc.
    # Generic system has: style: {background_color, text_color, icon}, kanban_display, etc.
    if result.stages:
        transformed_stages = []
        for stage in result.stages:
            # Extract style fields
            style = stage.get('style', {}) if isinstance(stage, dict) else getattr(stage, 'style', {})
            icon = style.get('icon', '📋') if isinstance(style, dict) else getattr(style, 'icon', '📋')
            background_color = style.get('background_color', '#E5E7EB') if isinstance(style, dict) else getattr(style,
                                                                                                                'background_color',
                                                                                                                '#E5E7EB')
            text_color = style.get('text_color', '#374151') if isinstance(style, dict) else getattr(style, 'text_color',
                                                                                                    '#374151')

            # Get other fields
            stage_id = stage.get('id') if isinstance(stage, dict) else getattr(stage, 'id', '')
            name = stage.get('name') if isinstance(stage, dict) else getattr(stage, 'name', '')
            kanban_display = stage.get('kanban_display', 'column') if isinstance(stage, dict) else getattr(stage,
                                                                                                           'kanban_display',
                                                                                                           'column')
            default_role_ids = stage.get('default_role_ids', []) if isinstance(stage, dict) else getattr(stage,
                                                                                                         'default_role_ids',
                                                                                                         [])
            role = default_role_ids[0] if default_role_ids else None

            # Map kanban_display values (generic: 'column'/'row'/'none' -> frontend: 'vertical'/'horizontal'/'hidden')
            kanban_display_map = {
                'column': 'vertical',
                'row': 'horizontal',
                'none': 'hidden'
            }
            kanban_display_mapped = kanban_display_map.get(kanban_display, kanban_display)

            # Create transformed stage
            transformed_stage = {
                'id': stage_id,
                'name': name,
                'icon': icon,
                'background_color': background_color,
                'text_color': text_color,
                'role': role,
                'status_mapping': 'draft',  # Default, as this doesn't exist in generic system
                'kanban_display': kanban_display_mapped,
                'field_visibility': {},  # Empty, as this doesn't exist in generic system
                'field_validation': stage.get('validation_rules', {}) if isinstance(stage, dict) else getattr(stage,
                                                                                                              'validation_rules',
                                                                                                              {}),
                'field_candidate_visibility': {}  # Empty, as this doesn't exist in generic system
            }
            transformed_stages.append(transformed_stage)

        result.stages = transformed_stages

    return result


@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
@inject
def update_workflow(
        workflow_id: str,
        controller: Annotated[
            WorkflowController, Depends(Provide[Container.candidate_application_workflow_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        body: dict = Body(...),
) -> WorkflowResponse:
    """Update a workflow (backward compatibility endpoint)
    
    Accepts both old format (JobPositionWorkflowUpdate with default_view, stages, custom_fields_config)
    and new format (UpdateWorkflowRequest with name, description, display, phase_id)
    """
    # Extract fields - handle both old and new formats
    name = body.get('name', '')
    description = body.get('description', '')

    # Handle display/default_view mapping
    display = body.get('display') or body.get('default_view')
    if display == 'kanban':
        display = 'kanban'
    elif display == 'list':
        display = 'list'
    else:
        display = None

    # Create UpdateWorkflowRequest with available fields
    update_request = UpdateWorkflowRequest(
        name=name,
        description=description or "",
        display=display,
        phase_id=body.get('phase_id')  # Phase ID if provided
    )

    # Update workflow using generic system
    # Note: update_workflow now returns enriched response with stages via WorkflowResponseService
    result = controller.update_workflow(workflow_id, update_request)

    # Note: stages and custom_fields_config from old format are ignored
    # These should be updated through separate stage endpoints or EntityCustomization system

    # Ensure stages is always a list (not None) for frontend compatibility
    if result.stages is None:
        result.stages = []

    # Transform stages to match frontend expected format (same as GET endpoint)
    if result.stages:
        transformed_stages = []
        for stage in result.stages:
            # Extract style fields
            style = stage.get('style', {}) if isinstance(stage, dict) else getattr(stage, 'style', {})
            icon = style.get('icon', '📋') if isinstance(style, dict) else getattr(style, 'icon', '📋')
            background_color = style.get('background_color', '#E5E7EB') if isinstance(style, dict) else getattr(style,
                                                                                                                'background_color',
                                                                                                                '#E5E7EB')
            text_color = style.get('text_color', '#374151') if isinstance(style, dict) else getattr(style, 'text_color',
                                                                                                    '#374151')

            # Get other fields
            stage_id = stage.get('id') if isinstance(stage, dict) else getattr(stage, 'id', '')
            name = stage.get('name') if isinstance(stage, dict) else getattr(stage, 'name', '')
            kanban_display = stage.get('kanban_display', 'column') if isinstance(stage, dict) else getattr(stage,
                                                                                                           'kanban_display',
                                                                                                           'column')
            default_role_ids = stage.get('default_role_ids', []) if isinstance(stage, dict) else getattr(stage,
                                                                                                         'default_role_ids',
                                                                                                         [])
            role = default_role_ids[0] if default_role_ids else None

            # Map kanban_display values (generic: 'column'/'row'/'none' -> frontend: 'vertical'/'horizontal'/'hidden')
            kanban_display_map = {
                'column': 'vertical',
                'row': 'horizontal',
                'none': 'hidden'
            }
            kanban_display_mapped = kanban_display_map.get(kanban_display, kanban_display)

            # Create transformed stage
            transformed_stage = {
                'id': stage_id,
                'name': name,
                'icon': icon,
                'background_color': background_color,
                'text_color': text_color,
                'role': role,
                'status_mapping': 'draft',  # Default, as this doesn't exist in generic system
                'kanban_display': kanban_display_mapped,
                'field_visibility': {},  # Empty, as this doesn't exist in generic system
                'field_validation': stage.get('validation_rules', {}) if isinstance(stage, dict) else getattr(stage,
                                                                                                              'validation_rules',
                                                                                                              {}),
                'field_candidate_visibility': {}  # Empty, as this doesn't exist in generic system
            }
            transformed_stages.append(transformed_stage)

        result.stages = transformed_stages

    return result


# Job Position Stage Management Endpoints

@router.post("/positions/{position_id}/move-to-stage", response_model=dict)
@inject
def move_position_to_stage(
        position_id: str,
        request: MoveJobPositionToStageRequest,
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> dict:
    """Move a job position to a new stage with validation"""
    from src.company_bc.job_position.application.commands.move_job_position_to_stage import JobPositionValidationError
    from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.company_bc.job_position.domain.value_objects import JobPositionId
    from src.company_bc.company.application.queries.get_company_user_by_company_and_user import \
        GetCompanyUserByCompanyAndUserQuery
    from fastapi import HTTPException

    try:
        # Get company_user_id for the current user
        from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
        from src.company_bc.company.application.dtos import CompanyUserDto

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

        return controller.move_position_to_stage(
            position_id=position_id,
            stage_id=request.stage_id,
            comment=request.comment,
            user_id=company_user_id
        )
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
        controller: Annotated[JobPositionController, Depends(Provide[Container.job_position_controller])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
) -> dict:
    """Update custom fields values for a job position"""
    return controller.update_custom_fields(
        position_id=position_id,
        custom_fields_values=request.custom_fields_values
    )


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
    from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.company_bc.job_position.domain.value_objects import JobPositionId
    from src.company_bc.company.application.queries.get_company_user_by_company_and_user import \
        GetCompanyUserByCompanyAndUserQuery

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
    from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.company_bc.job_position.domain.value_objects import JobPositionId
    from src.company_bc.company.application.queries.get_company_user_by_company_and_user import \
        GetCompanyUserByCompanyAndUserQuery

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
    from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.company_bc.job_position.domain.value_objects import JobPositionId
    from src.company_bc.company.application.queries.get_company_user_by_company_and_user import \
        GetCompanyUserByCompanyAndUserQuery

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


# ====================================
# MAINTENANCE ENDPOINTS
# ====================================

@router.post("/maintenance/cleanup-expired-registrations")
@inject
def cleanup_expired_registrations(
        command_bus: Annotated[CommandBus, Depends(Provide[Container.command_bus])],
        current_admin: Annotated[CurrentAdminUser, Depends(get_current_admin_user)],
        max_age_days: int = Query(7, ge=1, le=90, description="Max age in days for expired registrations"),
        dry_run: bool = Query(False, description="If true, only log what would be deleted"),
) -> dict:
    """
    Clean up expired user registrations.

    This endpoint deletes user registrations that:
    - Are in PENDING status with expired tokens
    - Are older than max_age_days

    Can be called manually or scheduled via external cron.
    """
    from src.auth_bc.user_registration.application.commands.cleanup_expired_registrations_command import (
        CleanupExpiredRegistrationsCommand
    )

    command = CleanupExpiredRegistrationsCommand(
        max_age_days=max_age_days,
        dry_run=dry_run
    )

    command_bus.dispatch(command)

    return {
        "status": "success",
        "message": f"Cleanup completed (dry_run={dry_run}, max_age_days={max_age_days})",
        "executed_by": current_admin.email
    }
