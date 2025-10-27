"""
Public Position Controller
Phase 10: Handles public job position operations
"""
from typing import Optional
import math

from src.job_position.application.queries.list_public_job_positions import (
    ListPublicJobPositionsQuery,
    ListPublicJobPositionsQueryHandler
)
from src.job_position.application.queries.get_public_job_position import (
    GetPublicJobPositionQuery,
    GetPublicJobPositionQueryHandler
)
from src.job_position.domain.exceptions import JobPositionNotFoundError
from src.job_position.presentation.schemas.public_position_schemas import (
    PublicPositionResponse,
    PublicPositionListResponse,
    SubmitApplicationRequest,
    SubmitApplicationResponse
)
from src.shared.application.query_bus import QueryBus


class PublicPositionController:
    """Controller for public job position operations"""

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def list_public_positions(
        self,
        search: Optional[str] = None,
        location: Optional[str] = None,
        department: Optional[str] = None,
        employment_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        is_remote: Optional[bool] = None,
        page: int = 1,
        page_size: int = 12
    ) -> PublicPositionListResponse:
        """
        List public job positions with filters

        Args:
            search: Search term for title/description
            location: Filter by location
            department: Filter by department
            employment_type: Filter by employment type
            experience_level: Filter by experience level
            is_remote: Filter remote positions
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            PublicPositionListResponse with positions and pagination info
        """
        # Calculate offset
        offset = (page - 1) * page_size

        # Create query
        query = ListPublicJobPositionsQuery(
            search_term=search,
            location=location,
            # department=department,  # Add if supported
            # contract_type=employment_type,  # Add enum conversion if needed
            limit=page_size,
            offset=offset
        )

        # Execute query
        position_dtos = self.query_bus.query(query)

        # Convert to response
        positions = [PublicPositionResponse.from_dto(dto) for dto in position_dtos]

        # Calculate total pages (simplified - in production, do a count query)
        total = len(positions)  # This is a simplification
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        return PublicPositionListResponse(
            positions=positions,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    def get_public_position(self, slug_or_id: str) -> PublicPositionResponse:
        """
        Get a single public job position by slug or ID

        Args:
            slug_or_id: Public slug or position ID

        Returns:
            PublicPositionResponse

        Raises:
            JobPositionNotFoundError: If position not found or not public
        """
        query = GetPublicJobPositionQuery(slug_or_id=slug_or_id)

        position_dto = self.query_bus.query(query)

        if not position_dto:
            raise JobPositionNotFoundError(f"Public position not found: {slug_or_id}")

        return PublicPositionResponse.from_dto(position_dto)

    def submit_application(
        self,
        slug_or_id: str,
        candidate_id: str,
        request: SubmitApplicationRequest
    ) -> SubmitApplicationResponse:
        """
        Submit an application to a public position

        Args:
            slug_or_id: Position slug or ID
            candidate_id: ID of the candidate applying
            request: Application request data

        Returns:
            SubmitApplicationResponse

        Note:
            This is a placeholder. Full implementation requires:
            - SubmitApplicationCommand
            - CompanyCandidate creation/linking
            - Workflow assignment
        """
        # TODO: Implement SubmitApplicationCommand in Phase 10 task 3
        # For now, return a placeholder response

        return SubmitApplicationResponse(
            application_id="placeholder-id",
            message="Application submission not yet implemented. Coming soon!"
        )
