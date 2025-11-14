from dataclasses import dataclass
from typing import Optional, List

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.company_bc.job_position.domain.enums import JobPositionStatusEnum, JobPositionVisibilityEnum
from src.company_bc.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.query_bus import Query
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListJobPositionsQuery(Query):
    """Query to list job positions - simplified (removed fields are in custom_fields_values)"""
    company_id: Optional[str] = None
    status: Optional[JobPositionStatusEnum] = None  # TODO: Filtering by status now requires workflow repository
    job_category: Optional[JobCategoryEnum] = None
    search_term: Optional[str] = None
    visibility: Optional[JobPositionVisibilityEnum] = None  # New filter for visibility
    limit: int = 50
    offset: int = 0
    current_user_id: Optional[str] = None  # For pending comments count with visibility filtering


@dataclass
class ListJobPositionsResult:
    """Result of listing job positions with total count"""
    positions: List[JobPositionDto]
    total: int


class ListJobPositionsQueryHandler:
    def __init__(
            self,
            job_position_repository: JobPositionRepositoryInterface,
            job_position_comment_repository: JobPositionCommentRepositoryInterface
    ):
        self.job_position_repository = job_position_repository
        self.job_position_comment_repository = job_position_comment_repository

    def handle(self, query: ListJobPositionsQuery) -> List[JobPositionDto]:
        """Handle query - simplified filters"""
        # Get total count with same filters (not used currently, but kept for future pagination)
        # total = self.job_position_repository.count_by_filters(
        #     company_id=query.company_id,
        #     status=query.status,
        #     job_category=query.job_category,
        #     search_term=query.search_term,
        #     visibility=query.visibility
        # )

        # Get paginated results
        jobPositions = self.job_position_repository.find_by_filters(
            company_id=query.company_id,
            status=query.status,  # TODO: This will require workflow repository to map stage to status
            job_category=query.job_category,
            search_term=query.search_term,
            visibility=query.visibility,
            limit=query.limit,
            offset=query.offset
        )

        # Convert to DTOs and add pending comments count
        dtos = []
        for jp in jobPositions:
            dto = JobPositionDto.from_entity(jp)

            # Count pending comments (with visibility filtering if current_user_id provided)
            if query.current_user_id:
                # Get all comments for this position that the user can see
                from src.company_bc.job_position.domain.enums import CommentReviewStatusEnum

                all_comments = self.job_position_comment_repository.list_by_job_position(
                    job_position_id=dto.id,
                    current_user_id=query.current_user_id
                )

                # Count how many are pending
                dto.pending_comments_count = sum(
                    1 for comment in all_comments
                    if comment.review_status == CommentReviewStatusEnum.PENDING
                )

            dtos.append(dto)

        return dtos
