"""Query for getting PDF analysis status."""

from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.framework.domain.dtos.resume_analysis_dto import AsyncJobStatusDto
from src.framework.domain.enums.async_job import AsyncJobType
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService


@dataclass
class GetPDFAnalysisStatusQuery(Query):
    """Query to get PDF analysis status by job ID."""
    job_id: str


@dataclass
class GetPDFAnalysisStatusByAssetQuery(Query):
    """Query to get PDF analysis status by user asset ID."""
    user_asset_id: str


class GetPDFAnalysisStatusQueryHandler(QueryHandler[GetPDFAnalysisStatusQuery, Optional[AsyncJobStatusDto]]):
    """Handler for GetPDFAnalysisStatusQuery."""

    def __init__(self, async_job_service: AsyncJobService):
        self.async_job_service = async_job_service

    def handle(self, query: GetPDFAnalysisStatusQuery) -> Optional[AsyncJobStatusDto]:
        """Handle the PDF analysis status query."""
        job_status = self.async_job_service.get_job_status(query.job_id)

        if not job_status:
            return None

        return AsyncJobStatusDto(
            job_id=job_status["job_id"],
            job_type=job_status["job_type"],
            status=job_status["status"],
            progress=job_status["progress"],
            message=job_status["message"],
            estimated_time_remaining=job_status["estimated_time_remaining"],
            started_at=job_status["started_at"],
            timeout_seconds=job_status["timeout_seconds"],
            created_at=job_status["created_at"],
            updated_at=job_status["updated_at"]
        )


class GetPDFAnalysisStatusByAssetQueryHandler(
    QueryHandler[GetPDFAnalysisStatusByAssetQuery, Optional[AsyncJobStatusDto]]):
    """Handler for GetPDFAnalysisStatusByAssetQuery."""

    def __init__(self, async_job_service: AsyncJobService):
        self.async_job_service = async_job_service

    def handle(self, query: GetPDFAnalysisStatusByAssetQuery) -> Optional[AsyncJobStatusDto]:
        """Handle the PDF analysis status query by asset ID."""
        job_info = self.async_job_service.get_job_by_entity(
            job_type=AsyncJobType.PDF_ANALYSIS,
            entity_type="user_asset",
            entity_id=query.user_asset_id
        )

        if not job_info:
            return None

        return AsyncJobStatusDto(
            job_id=job_info["job_id"],
            job_type=job_info["job_type"],
            status=job_info["status"],
            progress=job_info["progress"],
            message=job_info["message"],
            estimated_time_remaining=job_info["estimated_time_remaining"],
            started_at=job_info["started_at"],
            timeout_seconds=job_info["timeout_seconds"],
            created_at=job_info["created_at"],
            updated_at=job_info["updated_at"]
        )
