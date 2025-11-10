"""Candidate Review Controller."""
from typing import Optional, List

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.company_bc.candidate_review.application.commands.create_candidate_review_command import CreateCandidateReviewCommand
from src.company_bc.candidate_review.application.commands.update_candidate_review_command import UpdateCandidateReviewCommand
from src.company_bc.candidate_review.application.commands.delete_candidate_review_command import DeleteCandidateReviewCommand
from src.company_bc.candidate_review.application.commands.mark_review_as_reviewed_command import MarkReviewAsReviewedCommand
from src.company_bc.candidate_review.application.commands.mark_review_as_pending_command import MarkReviewAsPendingCommand
from src.company_bc.candidate_review.application.queries.get_review_by_id_query import GetReviewByIdQuery
from src.company_bc.candidate_review.application.queries.list_reviews_by_company_candidate_query import ListReviewsByCompanyCandidateQuery
from src.company_bc.candidate_review.application.queries.list_reviews_by_stage_query import ListReviewsByStageQuery
from src.company_bc.candidate_review.application.queries.list_global_reviews_query import ListGlobalReviewsQuery
from src.company_bc.candidate_review.presentation.schemas.create_review_request import CreateReviewRequest
from src.company_bc.candidate_review.presentation.schemas.update_review_request import UpdateReviewRequest
from src.company_bc.candidate_review.presentation.schemas.review_response import ReviewResponse
from src.company_bc.candidate_review.presentation.mappers.review_mapper import ReviewResponseMapper
from src.company_bc.candidate_review.domain.enums.review_status_enum import ReviewStatusEnum
from src.company_bc.candidate_review.domain.enums.review_score_enum import ReviewScoreEnum
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class ReviewController:
    """Controller for candidate review operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_review(self, company_candidate_id: str, request: CreateReviewRequest, created_by_user_id: str) -> ReviewResponse:
        """Create a new candidate review."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        # Validate score
        if request.score not in [0, 3, 6, 10]:
            raise ValueError("Score must be 0, 3, 6, or 10")

        # Generate review ID before executing command
        review_id = CandidateReviewId.generate()

        command = CreateCandidateReviewCommand(
            id=review_id,
            company_candidate_id=CompanyCandidateId.from_string(company_candidate_id),
            score=ReviewScoreEnum(request.score),
            created_by_user_id=CompanyUserId.from_string(created_by_user_id),
            comment=request.comment,
            workflow_id=WorkflowId.from_string(request.workflow_id) if request.workflow_id else None,
            stage_id=WorkflowStageId.from_string(request.stage_id) if request.stage_id else None,
            review_status=ReviewStatusEnum(request.review_status),
        )

        self._command_bus.dispatch(command)

        # Query directly by ID instead of listing all reviews
        from src.company_bc.candidate_review.application.queries.get_review_by_id_query import GetReviewByIdQuery
        query = GetReviewByIdQuery(review_id=review_id)
        dto: Optional[CandidateReviewDto] = self._query_bus.query(query)
        
        if not dto:
            raise Exception("Review not found after creation")

        return ReviewResponseMapper.dto_to_response(dto)

    def get_review_by_id(self, review_id: str) -> Optional[ReviewResponse]:
        """Get a candidate review by ID."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        query = GetReviewByIdQuery(review_id=CandidateReviewId.from_string(review_id))
        dto: Optional[CandidateReviewDto] = self._query_bus.query(query)

        if not dto:
            return None

        return ReviewResponseMapper.dto_to_response(dto)

    def list_reviews_by_company_candidate(self, company_candidate_id: str) -> List[ReviewResponse]:
        """Get all reviews for a company candidate."""
        query = ListReviewsByCompanyCandidateQuery(
            company_candidate_id=CompanyCandidateId.from_string(company_candidate_id)
        )
        dtos: List[CandidateReviewDto] = self._query_bus.query(query)

        return [ReviewResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_reviews_by_stage(self, company_candidate_id: str, stage_id: str) -> List[ReviewResponse]:
        """Get all reviews for a company candidate in a specific stage."""
        query = ListReviewsByStageQuery(
            company_candidate_id=CompanyCandidateId.from_string(company_candidate_id),
            stage_id=WorkflowStageId.from_string(stage_id)
        )
        dtos: List[CandidateReviewDto] = self._query_bus.query(query)

        return [ReviewResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_global_reviews(self, company_candidate_id: str) -> List[ReviewResponse]:
        """Get all global reviews for a company candidate."""
        query = ListGlobalReviewsQuery(
            company_candidate_id=CompanyCandidateId.from_string(company_candidate_id)
        )
        dtos: List[CandidateReviewDto] = self._query_bus.query(query)

        return [ReviewResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_review(self, review_id: str, request: UpdateReviewRequest) -> ReviewResponse:
        """Update a candidate review."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        # Validate score if provided
        if request.score is not None and request.score not in [0, 3, 6, 10]:
            raise ValueError("Score must be 0, 3, 6, or 10")

        command = UpdateCandidateReviewCommand(
            review_id=CandidateReviewId.from_string(review_id),
            score=ReviewScoreEnum(request.score) if request.score is not None else None,
            comment=request.comment,
        )

        self._command_bus.dispatch(command)

        query = GetReviewByIdQuery(review_id=CandidateReviewId.from_string(review_id))
        dto: Optional[CandidateReviewDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Review not found after update")

        return ReviewResponseMapper.dto_to_response(dto)

    def delete_review(self, review_id: str) -> None:
        """Delete a candidate review."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        command = DeleteCandidateReviewCommand(
            review_id=CandidateReviewId.from_string(review_id)
        )

        self._command_bus.dispatch(command)

    def mark_as_reviewed(self, review_id: str) -> ReviewResponse:
        """Mark a review as reviewed."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        command = MarkReviewAsReviewedCommand(
            review_id=CandidateReviewId.from_string(review_id)
        )

        self._command_bus.dispatch(command)

        query = GetReviewByIdQuery(review_id=CandidateReviewId.from_string(review_id))
        dto: Optional[CandidateReviewDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Review not found")

        return ReviewResponseMapper.dto_to_response(dto)

    def mark_as_pending(self, review_id: str) -> ReviewResponse:
        """Mark a review as pending."""
        from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
        
        command = MarkReviewAsPendingCommand(
            review_id=CandidateReviewId.from_string(review_id)
        )

        self._command_bus.dispatch(command)

        query = GetReviewByIdQuery(review_id=CandidateReviewId.from_string(review_id))
        dto: Optional[CandidateReviewDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Review not found")

        return ReviewResponseMapper.dto_to_response(dto)

