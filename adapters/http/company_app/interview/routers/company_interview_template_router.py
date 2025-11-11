"""Company Interview Template Router - For company users to manage their interview templates"""
import logging
from typing import List, Optional
import base64
import json

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from typing import Annotated

from core.container import Container
from adapters.http.admin_app.controllers.inverview_template_controller import InterviewTemplateController
from adapters.http.admin_app.schemas.interview_template import (
    InterviewTemplateResponse, InterviewTemplateCreate,
    InterviewTemplateSectionCreate, InterviewTemplateSectionUpdate,
    InterviewTemplateQuestionCreate, InterviewTemplateQuestionUpdate,
    InterviewTemplateQuestionResponse
)
from fastapi.security import OAuth2PasswordBearer

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/interview-templates", tags=["Company Interview Templates"])
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


def get_company_user_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_user_id from JWT token"""
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
        company_user_id = data.get('company_user_id')
        
        if not company_user_id or not isinstance(company_user_id, str):
            raise HTTPException(status_code=401, detail="company_user_id not found in token")
        
        return str(company_user_id)
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


# Interview Template CRUD

@router.get("", response_model=List[InterviewTemplateResponse])
@inject
def list_interview_templates(
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    search_term: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    job_category: Optional[str] = Query(None),
    page: Optional[int] = Query(None),
    page_size: Optional[int] = Query(None)
) -> List[InterviewTemplateResponse]:
    """List interview templates for the authenticated company"""
    # Filter by company_id (mandatory in company context)
    templates = controller.list_interview_templates(
        search_term=search_term,
        type=type,
        status=status,
        job_category=job_category,
        page=page,
        page_size=page_size,
        company_id=company_id  # Pass company_id to filter
    )
    return templates


@router.post("", response_model=InterviewTemplateResponse)
@inject
def create_interview_template(
    template_data: InterviewTemplateCreate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewTemplateResponse:
    """Create a new interview template for the authenticated company"""
    log.info(f"Creating interview template for company_id: {company_id}")
    if not company_id:
        raise HTTPException(status_code=400, detail="company_id is required")
    return controller.create_interview_template(
        template_data=template_data,
        current_admin_id=company_user_id,
        company_id=company_id  # Pass company_id (mandatory)
    )


@router.get("/{template_id}", response_model=InterviewTemplateResponse)
@inject
def get_interview_template(
    template_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
) -> InterviewTemplateResponse:
    """Get a specific interview template by ID (must belong to the company)"""
    template = controller.get_interview_template(template_id=template_id)
    
    # Verify template belongs to the company
    if not template.company_id or template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return template


@router.put("/{template_id}", response_model=InterviewTemplateResponse)
@inject
def update_interview_template(
    template_id: str,
    template_data: InterviewTemplateCreate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewTemplateResponse:
    """Update an existing interview template (must belong to the company)"""
    # Verify template belongs to the company before updating
    existing_template = controller.get_interview_template(template_id=template_id)
    if not existing_template.company_id or existing_template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return controller.update_interview_template(
        template_id=template_id,
        template_data=template_data,
        current_admin_id=company_user_id,
        company_id=company_id  # Pass company_id (mandatory)
    )


@router.post("/{template_id}/enable")
@inject
def enable_interview_template(
    template_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
    enable_reason: Optional[str] = None
) -> dict:
    """Enable an interview template (must belong to the company)"""
    # Verify template belongs to the company
    existing_template = controller.get_interview_template(template_id=template_id)
    if not existing_template.company_id or existing_template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return controller.enable_interview_template(
        template_id=template_id,
        current_admin_id=company_user_id,
        enable_reason=enable_reason
    )


@router.post("/{template_id}/disable")
@inject
def disable_interview_template(
    template_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
    disable_reason: Optional[str] = None,
    force_disable: bool = False
) -> dict:
    """Disable an interview template (must belong to the company)"""
    # Verify template belongs to the company
    existing_template = controller.get_interview_template(template_id=template_id)
    if not existing_template.company_id or existing_template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return controller.disable_interview_template(
        template_id=template_id,
        current_admin_id=company_user_id,
        disable_reason=disable_reason,
        force_disable=force_disable
    )


@router.delete("/{template_id}")
@inject
def delete_interview_template(
    template_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
    delete_reason: Optional[str] = Query(None),
    force_delete: bool = Query(False)
) -> dict:
    """Delete an interview template (must belong to the company)"""
    # Verify template belongs to the company
    existing_template = controller.get_interview_template(template_id=template_id)
    if not existing_template.company_id or existing_template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return controller.delete_interview_template(
        template_id=template_id,
        current_admin_id=company_user_id,
        delete_reason=delete_reason,
        force_delete=force_delete
    )


# Interview Template Section Management

@router.post("/sections", response_model=dict)
@inject
def create_interview_template_section(
    section_data: InterviewTemplateSectionCreate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Create a new interview template section (template must belong to the company)"""
    # Verify template belongs to the company
    existing_template = controller.get_interview_template(template_id=section_data.interview_template_id)
    if not existing_template.company_id or existing_template.company_id != company_id:
        raise HTTPException(status_code=404, detail="Interview template not found")
    
    return controller.create_interview_template_section(
        section_data=section_data,
        current_admin_id=company_user_id
    )


@router.put("/sections/{section_id}", response_model=dict)
@inject
def update_interview_template_section(
    section_id: str,
    section_data: InterviewTemplateSectionUpdate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Update an interview template section (template must belong to the company)"""
    # TODO: Verify section's template belongs to the company
    # For now, we'll rely on the controller to handle this
    return controller.update_interview_template_section(
        section_id=section_id,
        section_data=section_data,
        current_admin_id=company_user_id
    )


@router.post("/sections/{section_id}/enable", response_model=dict)
@inject
def enable_interview_template_section(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Enable an interview template section (template must belong to the company)"""
    return controller.enable_interview_template_section(
        section_id=section_id,
        current_admin_id=company_user_id
    )


@router.post("/sections/{section_id}/disable", response_model=dict)
@inject
def disable_interview_template_section(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Disable an interview template section (template must belong to the company)"""
    return controller.disable_interview_template_section(
        section_id=section_id,
        current_admin_id=company_user_id
    )


@router.delete("/sections/{section_id}", response_model=dict)
@inject
def delete_interview_template_section(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Delete an interview template section (template must belong to the company)"""
    return controller.delete_interview_template_section(
        section_id=section_id,
        current_admin_id=company_user_id
    )


@router.post("/sections/{section_id}/move-up", response_model=dict)
@inject
def move_section_up(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Move a section up in order (template must belong to the company)"""
    return controller.move_section_up(
        section_id=section_id,
        current_admin_id=company_user_id
    )


@router.post("/sections/{section_id}/move-down", response_model=dict)
@inject
def move_section_down(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Move a section down in order (template must belong to the company)"""
    return controller.move_section_down(
        section_id=section_id,
        current_admin_id=company_user_id
    )


# Interview Template Question Management

@router.get("/sections/{section_id}/questions", response_model=List[InterviewTemplateQuestionResponse])
@inject
def get_questions_by_section(
    section_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
) -> List[InterviewTemplateQuestionResponse]:
    """Get questions for a section (template must belong to the company)"""
    return controller.get_questions_by_section(section_id=section_id)


@router.post("/questions", response_model=dict)
@inject
def create_interview_template_question(
    question_data: InterviewTemplateQuestionCreate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Create a new interview template question (section's template must belong to the company)"""
    return controller.create_interview_template_question(question_data=question_data)


@router.put("/questions/{question_id}", response_model=dict)
@inject
def update_interview_template_question(
    question_id: str,
    question_data: InterviewTemplateQuestionUpdate,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Update an interview template question (section's template must belong to the company)"""
    return controller.update_interview_template_question(
        question_id=question_id,
        question_data=question_data,
        current_admin_id=company_user_id
    )


@router.post("/questions/{question_id}/enable", response_model=dict)
@inject
def enable_interview_template_question(
    question_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Enable an interview template question (section's template must belong to the company)"""
    return controller.enable_interview_template_question(
        question_id=question_id,
        current_admin_id=company_user_id
    )


@router.post("/questions/{question_id}/disable", response_model=dict)
@inject
def disable_interview_template_question(
    question_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Disable an interview template question (section's template must belong to the company)"""
    return controller.disable_interview_template_question(
        question_id=question_id,
        current_admin_id=company_user_id
    )


@router.delete("/questions/{question_id}", response_model=dict)
@inject
def delete_interview_template_question(
    question_id: str,
    controller: Annotated[InterviewTemplateController, Depends(Provide[Container.interview_template_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> dict:
    """Delete an interview template question (section's template must belong to the company)"""
    return controller.delete_interview_template_question(
        question_id=question_id,
        current_admin_id=company_user_id
    )

