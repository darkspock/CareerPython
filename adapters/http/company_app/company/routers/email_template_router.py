"""
Router for email template operations
Phase 7: Email Integration System
"""
from typing import Annotated, Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from adapters.http.company_app.company.controllers.email_template_controller import EmailTemplateController
from core.containers import Container
from src.notification_bc.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.notification_bc.email_template.domain.enums.trigger_event import TriggerEvent

router = APIRouter(
    prefix="/api/company/email-templates",
    tags=["company-email-templates"]
)


class CreateEmailTemplateRequest(BaseModel):
    """Request to create an email template"""
    workflow_id: str = Field(..., description="Workflow ID")
    template_name: str = Field(..., min_length=1, max_length=200, description="Template name")
    template_key: str = Field(..., min_length=1, max_length=100, description="Unique template key")
    subject: str = Field(..., min_length=1, max_length=500, description="Email subject")
    body_html: str = Field(..., min_length=1, description="HTML body")
    body_text: Optional[str] = Field(None, description="Plain text body")
    trigger_event: TriggerEvent = Field(..., description="Trigger event")
    available_variables: List[str] = Field(..., description="Available template variables")
    stage_id: Optional[str] = Field(None, description="Stage ID (if stage-specific)")
    is_active: bool = Field(True, description="Whether template is active")


class UpdateEmailTemplateRequest(BaseModel):
    """Request to update an email template"""
    template_name: str = Field(..., min_length=1, max_length=200, description="Template name")
    subject: str = Field(..., min_length=1, max_length=500, description="Email subject")
    body_html: str = Field(..., min_length=1, description="HTML body")
    body_text: Optional[str] = Field(None, description="Plain text body")
    available_variables: List[str] = Field(..., description="Available template variables")


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
def create_email_template(
        request: CreateEmailTemplateRequest,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> dict:
    """
    Create a new email template.

    Phase 7: Email Integration - Creates a new email template for a workflow.
    Templates can be triggered by various events like stage transitions, status changes, etc.
    """
    try:
        result = controller.create_template(
            workflow_id=request.workflow_id,
            template_name=request.template_name,
            template_key=request.template_key,
            subject=request.subject,
            body_html=request.body_html,
            trigger_event=request.trigger_event,
            available_variables=request.available_variables,
            stage_id=request.stage_id,
            body_text=request.body_text,
            is_active=request.is_active
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create email template: {str(e)}"
        )


@router.get("/{template_id}", status_code=status.HTTP_200_OK)
@inject
def get_email_template(
        template_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> EmailTemplateDto:
    """
    Get an email template by ID.

    Phase 7: Email Integration - Retrieves a specific email template.
    """
    try:
        template = controller.get_template_by_id(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email template not found"
            )
        return template

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get email template: {str(e)}"
        )


@router.put("/{template_id}", status_code=status.HTTP_200_OK)
@inject
def update_email_template(
        template_id: str,
        request: UpdateEmailTemplateRequest,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> dict:
    """
    Update an existing email template.

    Phase 7: Email Integration - Updates template content and configuration.
    """
    try:
        result = controller.update_template(
            template_id=template_id,
            template_name=request.template_name,
            subject=request.subject,
            body_html=request.body_html,
            available_variables=request.available_variables,
            body_text=request.body_text
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update email template: {str(e)}"
        )


@router.delete("/{template_id}", status_code=status.HTTP_200_OK)
@inject
def delete_email_template(
        template_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> dict:
    """
    Delete an email template.

    Phase 7: Email Integration - Permanently deletes an email template.
    """
    try:
        result = controller.delete_template(template_id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete email template: {str(e)}"
        )


@router.post("/{template_id}/activate", status_code=status.HTTP_200_OK)
@inject
def activate_email_template(
        template_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> dict:
    """
    Activate an email template.

    Phase 7: Email Integration - Activates a template so it can be triggered.
    """
    try:
        result = controller.activate_template(template_id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to activate email template: {str(e)}"
        )


@router.post("/{template_id}/deactivate", status_code=status.HTTP_200_OK)
@inject
def deactivate_email_template(
        template_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])]
) -> dict:
    """
    Deactivate an email template.

    Phase 7: Email Integration - Deactivates a template so it won't be triggered.
    """
    try:
        result = controller.deactivate_template(template_id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deactivate email template: {str(e)}"
        )


@router.get("/workflow/{workflow_id}", status_code=status.HTTP_200_OK)
@inject
def list_templates_by_workflow(
        workflow_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])],
        active_only: bool = Query(False, description="Return only active templates"),
) -> List[EmailTemplateDto]:
    """
    List all email templates for a workflow.

    Phase 7: Email Integration - Retrieves all templates configured for a workflow.
    """
    try:
        templates = controller.list_templates_by_workflow(
            workflow_id=workflow_id,
            active_only=active_only
        )
        return templates

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list email templates: {str(e)}"
        )


@router.get("/stage/{stage_id}", status_code=status.HTTP_200_OK)
@inject
def list_templates_by_stage(
        stage_id: str,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])],
        active_only: bool = Query(False, description="Return only active templates"),
) -> List[EmailTemplateDto]:
    """
    List all email templates for a stage.

    Phase 7: Email Integration - Retrieves all templates configured for a specific stage.
    """
    try:
        templates = controller.list_templates_by_stage(
            stage_id=stage_id,
            active_only=active_only
        )
        return templates

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list email templates: {str(e)}"
        )


@router.get("/trigger/{workflow_id}/{trigger_event}", status_code=status.HTTP_200_OK)
@inject
def get_templates_by_trigger(
        workflow_id: str,
        trigger_event: TriggerEvent,
        controller: Annotated[EmailTemplateController, Depends(Provide[Container.email_template_controller])],
        stage_id: Optional[str] = Query(None, description="Filter by stage ID"),
        active_only: bool = Query(True, description="Return only active templates"),
) -> List[EmailTemplateDto]:
    """
    Get templates by trigger event.

    Phase 7: Email Integration - Retrieves templates that should be sent for a specific trigger.
    This is the key endpoint used by event handlers to find which emails to send.
    """
    try:
        templates = controller.get_templates_by_trigger(
            workflow_id=workflow_id,
            trigger_event=trigger_event,
            stage_id=stage_id,
            active_only=active_only
        )
        return templates

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get email templates by trigger: {str(e)}"
        )
