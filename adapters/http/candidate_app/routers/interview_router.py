"""Candidate Interview Router - For candidates to access interviews via secure links"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query

from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.company_app.interview.schemas.interview_management import InterviewManagementResponse
from adapters.http.candidate_app.schemas.interview_public import (
    InterviewQuestionsPublicResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse
)
from core.container import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/candidate/interviews", tags=["Candidate Interviews"])


@router.get("/{interview_id}/access", response_model=InterviewManagementResponse)
@inject
def access_interview_by_token(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        token: str = Query(..., description="Secure token for interview access"),
) -> InterviewManagementResponse:
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
