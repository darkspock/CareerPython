from typing import List, Optional, Dict, Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from adapters.http.company_app.company_candidate.controllers.company_candidate_controller import \
    CompanyCandidateController
from adapters.http.company_app.company_candidate.schemas.assign_workflow_request import AssignWorkflowRequest
from adapters.http.company_app.company_candidate.schemas.change_stage_request import ChangeStageRequest
from adapters.http.company_app.company_candidate.schemas.company_candidate_response import CompanyCandidateResponse
from adapters.http.company_app.company_candidate.schemas.create_company_candidate_request import \
    CreateCompanyCandidateRequest
from adapters.http.company_app.company_candidate.schemas.update_company_candidate_request import \
    UpdateCompanyCandidateRequest
from core.containers import Container
from src.framework.application.query_bus import QueryBus

router = APIRouter(
    prefix="/api/company-candidates",
    tags=["company-candidates"]
)


@router.post(
    "/",
    response_model=CompanyCandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company candidate relationship"
)
@inject
async def create_company_candidate(
        request: CreateCompanyCandidateRequest,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Create a new company candidate relationship"""
    print(f"[DEBUG] Received request type: {type(request)}")
    print(f"[DEBUG] Request data: {request}")
    try:
        return controller.create_company_candidate(request)
    except Exception as e:
        print(f"[DEBUG] Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{company_candidate_id}",
    response_model=CompanyCandidateResponse,
    summary="Get a company candidate by ID"
)
@inject
def get_company_candidate_by_id(
        company_candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> Optional[CompanyCandidateResponse]:
    """Get a company candidate by ID"""
    result = controller.get_company_candidate_by_id(company_candidate_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
    return result


@router.get(
    "/company/{company_id}/candidate/{candidate_id}",
    response_model=CompanyCandidateResponse,
    summary="Get a company candidate by company ID and candidate ID"
)
@inject
def get_company_candidate_by_company_and_candidate(
        company_id: str,
        candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> Optional[CompanyCandidateResponse]:
    """Get a company candidate by company ID and candidate ID"""
    result = controller.get_company_candidate_by_company_and_candidate(company_id, candidate_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company candidate not found")
    return result


@router.get(
    "/company/{company_id}",
    response_model=List[CompanyCandidateResponse],
    summary="List all company candidates for a specific company"
)
@inject
def list_company_candidates_by_company(
        company_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> List[CompanyCandidateResponse]:
    """List all company candidates for a specific company"""
    return controller.list_company_candidates_by_company(company_id)


@router.get(
    "/candidate/{candidate_id}",
    response_model=List[CompanyCandidateResponse],
    summary="List all company candidates for a specific candidate"
)
@inject
def list_company_candidates_by_candidate(
        candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> List[CompanyCandidateResponse]:
    """List all company candidates for a specific candidate"""
    return controller.list_company_candidates_by_candidate(candidate_id)


@router.put(
    "/{company_candidate_id}",
    response_model=CompanyCandidateResponse,
    summary="Update company candidate information"
)
@inject
def update_company_candidate(
        company_candidate_id: str,
        request: UpdateCompanyCandidateRequest,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Update company candidate information"""
    try:
        return controller.update_company_candidate(company_candidate_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/confirm",
    response_model=CompanyCandidateResponse,
    summary="Candidate confirms/accepts company invitation"
)
@inject
def confirm_company_candidate(
        company_candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Candidate confirms/accepts company invitation"""
    try:
        return controller.confirm_company_candidate(company_candidate_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/reject",
    response_model=CompanyCandidateResponse,
    summary="Candidate rejects/declines company invitation"
)
@inject
def reject_company_candidate(
        company_candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Candidate rejects/declines company invitation"""
    try:
        return controller.reject_company_candidate(company_candidate_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/archive",
    response_model=CompanyCandidateResponse,
    summary="Archive a company candidate relationship"
)
@inject
def archive_company_candidate(
        company_candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Archive a company candidate relationship"""
    try:
        return controller.archive_company_candidate(company_candidate_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/transfer-ownership",
    response_model=CompanyCandidateResponse,
    summary="Transfer ownership from company to user"
)
@inject
def transfer_ownership(
        company_candidate_id: str,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Transfer ownership from company to user"""
    try:
        return controller.transfer_ownership(company_candidate_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/assign-workflow",
    response_model=CompanyCandidateResponse,
    summary="Assign a workflow to a company candidate"
)
@inject
def assign_workflow(
        company_candidate_id: str,
        request: AssignWorkflowRequest,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Assign a workflow to a company candidate"""
    try:
        return controller.assign_workflow(company_candidate_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{company_candidate_id}/change-stage",
    response_model=CompanyCandidateResponse,
    summary="Change the workflow stage of a company candidate"
)
@inject
def change_stage(
        company_candidate_id: str,
        request: ChangeStageRequest,
        controller: CompanyCandidateController = Depends(Provide[Container.company_candidate_controller])
) -> CompanyCandidateResponse:
    """Change the workflow stage of a company candidate"""
    try:
        return controller.change_stage(company_candidate_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ============================================================================
# Candidate Report Generation
# ============================================================================

class GenerateReportRequest(BaseModel):
    """Request to generate a candidate report"""
    company_candidate_id: str = Field(..., description="Company candidate ID")
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


@router.post(
    "/reports/generate",
    response_model=CandidateReportResponse,
    summary="Generate AI-powered candidate report"
)
@inject
def generate_candidate_report(
        request: GenerateReportRequest,
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
        query = GenerateCandidateReportQuery(
            company_candidate_id=request.company_candidate_id,
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
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )
