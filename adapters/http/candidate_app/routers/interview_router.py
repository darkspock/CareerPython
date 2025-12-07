"""Candidate Interview Router - For candidates to access interviews via secure links"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.company_app.interview.schemas.interview_management import InterviewFullResource
from src.framework.infrastructure.services.calendar import ICSService, ICSEvent
from adapters.http.candidate_app.schemas.interview_public import (
    InterviewQuestionsPublicResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    AIFollowUpRequest,
    AIFollowUpResponse
)
from src.framework.infrastructure.services.ai.groq_chat_service import get_chat_service, ChatMessage
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/candidate/interviews", tags=["Candidate Interviews"])


@router.get("/{interview_id}/access", response_model=InterviewFullResource)
@inject
def access_interview_by_token(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> InterviewFullResource:
    """
    Access interview by secure token link.
    This endpoint allows candidates to access their interviews using a secure token.
    The token is validated and must not be expired.
    """
    try:
        response = controller.get_interview_by_token(
            interview_id=interview_id,
            token=token
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error accessing interview {interview_id} by token: {e}")
        raise HTTPException(status_code=404, detail="Interview not found or token is invalid/expired")


@router.get("/{interview_id}/questions", response_model=InterviewQuestionsPublicResponse)
@inject
def get_interview_questions_by_token(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> InterviewQuestionsPublicResponse:
    """
    Get interview questions by secure token link.
    This endpoint allows candidates and interviewers to access interview questions using a secure token.
    Returns the interview template with all sections and questions, plus existing answers.
    """
    try:
        result = controller.get_interview_questions_by_token(
            interview_id=interview_id,
            token=token
        )

        # Convert DTO to public response
        template_response = None
        if result.template:
            from adapters.http.candidate_app.schemas.interview_public import (
                InterviewTemplatePublicResponse,
                InterviewSectionPublicResponse,
                InterviewQuestionPublicResponse
            )

            sections = []
            for section_dto in result.template.sections:
                questions = []
                for question_dto in section_dto.questions:
                    questions.append(InterviewQuestionPublicResponse(
                        id=question_dto.id.value,
                        name=question_dto.name,
                        description=question_dto.description,
                        code=question_dto.code,
                        sort_order=question_dto.sort_order,
                        interview_template_section_id=question_dto.interview_template_section_id.value,
                        scope=question_dto.scope.value if question_dto.scope else None,
                        data_type=question_dto.data_type.value if question_dto.data_type else None,
                        status=question_dto.status.value if question_dto.status else None,
                        allow_ai_followup=question_dto.allow_ai_followup,
                        legal_notice=question_dto.legal_notice
                    ))

                sections.append(InterviewSectionPublicResponse(
                    id=section_dto.id,
                    name=section_dto.name,
                    intro=section_dto.intro,
                    prompt=section_dto.prompt,
                    goal=section_dto.goal,
                    sort_order=section_dto.sort_order,
                    section=section_dto.section.value if section_dto.section else None,
                    status=section_dto.status.value if section_dto.status else None,
                    questions=questions
                ))

            template_response = InterviewTemplatePublicResponse(
                id=result.template.id.value,
                name=result.template.name,
                intro=result.template.intro,
                prompt=result.template.prompt,
                goal=result.template.goal,
                scoring_mode=result.template.scoring_mode.value if result.template.scoring_mode else None,
                sections=sections
            )

        return InterviewQuestionsPublicResponse(
            interview_id=result.interview_id,
            interview_title=result.interview_title,
            interview_description=result.interview_description,
            scheduled_at=result.scheduled_at,
            template=template_response,
            existing_answers=result.existing_answers
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting interview questions for {interview_id} by token: {e}")
        raise HTTPException(status_code=404, detail="Interview not found or token is invalid/expired")


@router.post("/{interview_id}/answers", response_model=SubmitAnswerResponse)
@inject
def submit_interview_answer_by_token(
        interview_id: str,
        answer_data: SubmitAnswerRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> SubmitAnswerResponse:
    """
    Submit interview answer by secure token link.
    This endpoint allows candidates and interviewers to submit answers using a secure token.
    Creates a new answer if it doesn't exist, or updates existing answer.
    """
    try:
        result = controller.submit_interview_answer_by_token(
            interview_id=interview_id,
            token=token,
            question_id=answer_data.question_id,
            answer_text=answer_data.answer_text,
            question_text=answer_data.question_text
        )

        return SubmitAnswerResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error submitting answer for interview {interview_id} by token: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ai/follow-up", response_model=AIFollowUpResponse)
def generate_ai_followup(
    request: AIFollowUpRequest,
) -> AIFollowUpResponse:
    """
    Generate an AI-powered follow-up question based on the candidate's response.
    This endpoint uses Groq AI to generate contextual follow-up questions.
    """
    try:
        # Get AI chat service
        ai_service = get_chat_service()

        # Build conversation history if provided
        previous_messages = None
        if request.conversation_history:
            previous_messages = [
                ChatMessage(role=msg.get("role", "user"), content=msg.get("content", ""))
                for msg in request.conversation_history
            ]

        # Generate follow-up
        response = ai_service.generate_interview_followup(
            question=request.question,
            candidate_response=request.candidate_response,
            position_context=request.position_context,
            previous_messages=previous_messages
        )

        if response.success:
            return AIFollowUpResponse(
                follow_up_question=response.content,
                success=True
            )
        else:
            log.warning(f"AI follow-up generation failed: {response.error_message}")
            return AIFollowUpResponse(
                follow_up_question="Could you elaborate more on that? Can you provide a specific example?",
                success=False,
                error_message=response.error_message
            )

    except Exception as e:
        log.error(f"Error generating AI follow-up: {e}")
        # Return a fallback question instead of failing completely
        return AIFollowUpResponse(
            follow_up_question="That's interesting. Could you tell me more about your experience with that?",
            success=False,
            error_message=str(e)
        )


# ============================================================================
# Calendar Export Endpoints (for candidates)
# ============================================================================

@router.get("/{interview_id}/calendar.ics")
@inject
def download_candidate_interview_ics(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> Response:
    """Download an interview as an .ics calendar file (for candidates)"""
    try:
        # Validate token and get interview details
        interview = controller.get_interview_by_token(
            interview_id=interview_id,
            token=token
        )

        if not interview.scheduled_at:
            raise HTTPException(
                status_code=400,
                detail="Interview is not scheduled yet"
            )

        # Build event description for candidate
        description_parts = []
        if interview.description:
            description_parts.append(interview.description)
        if interview.title:
            description_parts.append(f"Interview: {interview.title}")
        if interview.job_position_title:
            description_parts.append(f"Position: {interview.job_position_title}")
        if interview.interview_type:
            description_parts.append(f"Type: {interview.interview_type}")

        # Create ICS event
        event = ICSEvent(
            uid=f"interview-{interview_id}@careerpython.com",
            summary=interview.title or "Job Interview",
            start=interview.scheduled_at,
            end=interview.deadline_date,
            description="\n".join(description_parts) if description_parts else None,
        )

        # Generate ICS content
        ics_service = ICSService()
        ics_content = ics_service.generate_event(event)

        # Return as downloadable file
        filename = f"interview-{interview_id}.ics"
        return Response(
            content=ics_content,
            media_type="text/calendar",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "text/calendar; charset=utf-8"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error generating ICS for candidate interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate calendar file")


@router.get("/{interview_id}/calendar-links")
@inject
def get_candidate_interview_calendar_links(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> dict:
    """Get calendar links for a candidate's interview (Google Calendar, Outlook, etc.)"""
    try:
        # Validate token and get interview details
        interview = controller.get_interview_by_token(
            interview_id=interview_id,
            token=token
        )

        if not interview.scheduled_at:
            raise HTTPException(
                status_code=400,
                detail="Interview is not scheduled yet"
            )

        # Build event description
        description_parts = []
        if interview.description:
            description_parts.append(interview.description)
        if interview.job_position_title:
            description_parts.append(f"Position: {interview.job_position_title}")

        # Create ICS event for URL generation
        event = ICSEvent(
            uid=f"interview-{interview_id}@careerpython.com",
            summary=interview.title or "Job Interview",
            start=interview.scheduled_at,
            end=interview.deadline_date,
            description="\n".join(description_parts) if description_parts else None,
        )

        # Generate calendar URLs
        ics_service = ICSService()

        return {
            "google_calendar_url": ics_service.generate_google_calendar_url(event),
            "outlook_url": ics_service.generate_outlook_url(event),
            "ics_download_url": f"/api/candidate/interviews/{interview_id}/calendar.ics?token={token}",
            "interview_id": interview_id,
            "scheduled_at": interview.scheduled_at.isoformat() if interview.scheduled_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error generating calendar links for candidate interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate calendar links")
