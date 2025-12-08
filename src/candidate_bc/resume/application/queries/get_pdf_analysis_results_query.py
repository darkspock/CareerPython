"""Query for getting PDF analysis results."""

from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.framework.application.dtos.resume_analysis_dto import AsyncJobResultDto
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService


@dataclass
class GetPDFAnalysisResultsQuery(Query):
    """Query to get PDF analysis results by job ID."""
    job_id: str


class GetPDFAnalysisResultsQueryHandler(QueryHandler[GetPDFAnalysisResultsQuery, Optional[AsyncJobResultDto]]):
    """Handler for GetPDFAnalysisResultsQuery."""

    def __init__(self, async_job_service: AsyncJobService):
        self.async_job_service = async_job_service

    def handle(self, query: GetPDFAnalysisResultsQuery) -> Optional[AsyncJobResultDto]:
        """Handle the PDF analysis results query."""
        job_results = self.async_job_service.get_job_results(query.job_id)

        if not job_results:
            return None

        return AsyncJobResultDto(
            job_id=job_results["job_id"],
            job_type=job_results["job_type"],
            status=job_results["status"],
            success=job_results["success"],
            results=job_results["results"],
            error_message=job_results["error_message"],
            completed_at=job_results["completed_at"]
        )
