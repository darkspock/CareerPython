"""
Public Position Controller
Phase 10: Handles public job position operations
"""
import math
from typing import Optional, List

from adapters.http.admin.mappers.job_position_mapper import JobPositionMapper
from src.company_bc.job_position.application.queries.get_public_job_position import (
    GetPublicJobPositionQuery
)
from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.company_bc.job_position.application.queries.list_public_job_positions import (
    ListPublicJobPositionsQuery
)
from src.company_bc.job_position.domain import JobPositionNotFoundError
from src.company_bc.job_position.presentation.schemas.public_position_schemas import (
    PublicPositionResponse,
    PublicPositionListResponse,
    SubmitApplicationRequest,
    SubmitApplicationResponse
)
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.workflow.application import WorkflowDto
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.shared_bc.customization.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQuery
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


class PublicPositionController:
    """Controller for public job position operations"""

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def list_public_positions(
            self,
            search: Optional[str] = None,
            page: int = 1,
            page_size: int = 12
    ) -> PublicPositionListResponse:
        """
        List public job positions with filters - simplified

        Args:
            search: Search term for title/description
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
            limit=page_size,
            offset=offset
        )

        # Execute query
        position_dtos: List[JobPositionDto] = self.query_bus.query(query)

        # Convert to response - get workflow for each position to filter visible fields
        positions = []
        for dto in position_dtos:
            # Try to get workflow and stages if available
            workflow_dto: Optional[WorkflowDto] = None
            stages = None
            if dto.job_position_workflow_id:
                try:
                    workflow_query = GetWorkflowByIdQuery(
                        id=WorkflowId.from_string(dto.job_position_workflow_id)
                    )
                    workflow_result: Optional[WorkflowDto] = self.query_bus.query(workflow_query)
                    workflow_dto = workflow_result

                    # Get stages for the workflow
                    if workflow_result is not None:
                        stages_query = ListStagesByWorkflowQuery(
                            workflow_id=WorkflowId.from_string(workflow_result.id)
                        )
                        stages = self.query_bus.query(stages_query)
                except Exception:
                    # If workflow not found, continue without it
                    pass

            # Use mapper to get only visible fields for candidates
            public_response = JobPositionMapper.dto_to_public_response(dto, workflow_dto, stages)
            positions.append(PublicPositionResponse.from_public_response(public_response))

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
        Get a single public job position by slug or ID - only visible fields for candidates

        Args:
            slug_or_id: Public slug or position ID

        Returns:
            PublicPositionResponse with only visible fields

        Raises:
            JobPositionNotFoundError: If position not found or not public
        """
        query = GetPublicJobPositionQuery(slug_or_id=slug_or_id)

        position_dto: JobPositionDto = self.query_bus.query(query)

        if not position_dto:
            raise JobPositionNotFoundError(f"Public position not found: {slug_or_id}")

        # Get workflow and stages if available to filter visible fields
        workflow_dto: Optional[WorkflowDto] = None
        stages = None
        if position_dto.job_position_workflow_id:
            try:
                workflow_query = GetWorkflowByIdQuery(
                    id=WorkflowId.from_string(position_dto.job_position_workflow_id)
                )
                workflow_result: Optional[WorkflowDto] = self.query_bus.query(workflow_query)
                workflow_dto = workflow_result

                # Get stages for the workflow
                if workflow_result is not None:
                    stages_query = ListStagesByWorkflowQuery(
                        workflow_id=WorkflowId.from_string(workflow_result.id)
                    )
                    stages = self.query_bus.query(stages_query)
            except Exception:
                # If workflow not found, continue without it
                pass

        # Use mapper to get only visible fields for candidates
        public_response = JobPositionMapper.dto_to_public_response(position_dto, workflow_dto, stages)
        return PublicPositionResponse.from_public_response(public_response)

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

