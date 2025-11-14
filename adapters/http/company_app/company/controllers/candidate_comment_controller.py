"""Candidate Comment Controller."""
from typing import Optional, List

import ulid

from adapters.http.company_app.company_candidate.mappers.candidate_comment_mapper import CandidateCommentResponseMapper
from adapters.http.company_app.company_candidate.schemas.candidate_comment_response import CandidateCommentResponse
from adapters.http.company_app.company_candidate.schemas.create_candidate_comment_request import \
    CreateCandidateCommentRequest
from adapters.http.company_app.company_candidate.schemas.update_candidate_comment_request import \
    UpdateCandidateCommentRequest
from src.company_bc.company_candidate.application.commands.create_candidate_comment_command import \
    CreateCandidateCommentCommand
from src.company_bc.company_candidate.application.commands.delete_candidate_comment_command import \
    DeleteCandidateCommentCommand
from src.company_bc.company_candidate.application.commands.mark_comment_as_pending_command import \
    MarkCommentAsPendingCommand
from src.company_bc.company_candidate.application.commands.mark_comment_as_reviewed_command import \
    MarkCandidateCommentAsReviewedCommand
from src.company_bc.company_candidate.application.commands.update_candidate_comment_command import \
    UpdateCandidateCommentCommand
from src.company_bc.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto
from src.company_bc.company_candidate.application.queries.count_pending_comments_query import CountPendingCommentsQuery
from src.company_bc.company_candidate.application.queries.get_candidate_comment_by_id import \
    GetCandidateCommentByIdQuery
from src.company_bc.company_candidate.application.queries.list_candidate_comments_by_company_candidate import \
    ListCandidateCommentsByCompanyCandidateQuery
from src.company_bc.company_candidate.application.queries.list_candidate_comments_by_stage import \
    ListCandidateCommentsByStageQuery
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class CandidateCommentController:
    """Controller for candidate comment operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_comment(self, company_candidate_id: str, request: CreateCandidateCommentRequest,
                       created_by_user_id: str) -> CandidateCommentResponse:
        """Create a new candidate comment."""
        comment_id = str(ulid.new())

        command = CreateCandidateCommentCommand(
            id=comment_id,
            company_candidate_id=company_candidate_id,
            comment=request.comment,
            created_by_user_id=created_by_user_id,
            workflow_id=request.workflow_id,
            stage_id=request.stage_id,
            visibility=request.visibility,
            review_status=request.review_status
        )

        self._command_bus.dispatch(command)

        query = GetCandidateCommentByIdQuery(id=comment_id)
        dto: Optional[CandidateCommentDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Comment not found after creation")

        return CandidateCommentResponseMapper.dto_to_response(dto)

    def get_comment_by_id(self, comment_id: str) -> Optional[CandidateCommentResponse]:
        """Get a candidate comment by ID."""
        query = GetCandidateCommentByIdQuery(id=comment_id)
        dto: Optional[CandidateCommentDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CandidateCommentResponseMapper.dto_to_response(dto)

    def list_comments_by_company_candidate(self, company_candidate_id: str) -> List[CandidateCommentResponse]:
        """Get all comments for a company candidate."""
        query = ListCandidateCommentsByCompanyCandidateQuery(company_candidate_id=company_candidate_id)
        dtos: List[CandidateCommentDto] = self._query_bus.query(query)

        return [CandidateCommentResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_comments_by_stage(self, company_candidate_id: str, stage_id: str) -> List[CandidateCommentResponse]:
        """Get all comments for a company candidate in a specific stage."""
        query = ListCandidateCommentsByStageQuery(
            company_candidate_id=company_candidate_id,
            stage_id=stage_id
        )
        dtos: List[CandidateCommentDto] = self._query_bus.query(query)

        return [CandidateCommentResponseMapper.dto_to_response(dto) for dto in dtos]

    def count_pending_comments(self, company_candidate_id: str) -> int:
        """Count pending comments for a company candidate."""
        query = CountPendingCommentsQuery(company_candidate_id=company_candidate_id)
        return self._query_bus.query(query)

    def update_comment(self, comment_id: str, request: UpdateCandidateCommentRequest) -> Optional[
        CandidateCommentResponse]:
        """Update a candidate comment."""
        command = UpdateCandidateCommentCommand(
            id=comment_id,
            comment=request.comment,
            visibility=request.visibility
        )

        self._command_bus.dispatch(command)

        # Return updated comment
        query = GetCandidateCommentByIdQuery(id=comment_id)
        dto: Optional[CandidateCommentDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CandidateCommentResponseMapper.dto_to_response(dto)

    def delete_comment(self, comment_id: str) -> None:
        """Delete a candidate comment."""
        command = DeleteCandidateCommentCommand(id=comment_id)
        self._command_bus.dispatch(command)

    def mark_as_pending(self, comment_id: str) -> Optional[CandidateCommentResponse]:
        """Mark a comment as pending review."""
        command = MarkCommentAsPendingCommand(id=comment_id)
        self._command_bus.dispatch(command)

        query = GetCandidateCommentByIdQuery(id=comment_id)
        dto: Optional[CandidateCommentDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CandidateCommentResponseMapper.dto_to_response(dto)

    def mark_as_reviewed(self, comment_id: str) -> Optional[CandidateCommentResponse]:
        """Mark a comment as reviewed."""
        command = MarkCandidateCommentAsReviewedCommand(id=comment_id)
        self._command_bus.dispatch(command)

        query = GetCandidateCommentByIdQuery(id=comment_id)
        dto: Optional[CandidateCommentDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CandidateCommentResponseMapper.dto_to_response(dto)
