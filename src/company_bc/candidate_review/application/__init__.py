"""Candidate review application module - exports queries and commands"""

# Queries
from .queries.get_review_by_id_query import GetReviewByIdQuery, GetReviewByIdQueryHandler
from .queries.list_global_reviews_query import ListGlobalReviewsQuery, ListGlobalReviewsQueryHandler
from .queries.list_reviews_by_company_candidate_query import (
    ListReviewsByCompanyCandidateQuery,
    ListReviewsByCompanyCandidateQueryHandler,
)
from .queries.list_reviews_by_stage_query import ListReviewsByStageQuery, ListReviewsByStageQueryHandler

# Commands
from .commands.create_candidate_review_command import (
    CreateCandidateReviewCommand,
    CreateCandidateReviewCommandHandler,
)
from .commands.delete_candidate_review_command import (
    DeleteCandidateReviewCommand,
    DeleteCandidateReviewCommandHandler,
)
from .commands.mark_review_as_pending_command import (
    MarkReviewAsPendingCommand,
    MarkReviewAsPendingCommandHandler,
)
from .commands.mark_review_as_reviewed_command import (
    MarkReviewAsReviewedCommand,
    MarkReviewAsReviewedCommandHandler,
)
from .commands.update_candidate_review_command import (
    UpdateCandidateReviewCommand,
    UpdateCandidateReviewCommandHandler,
)

__all__ = [
    # Queries
    "GetReviewByIdQuery",
    "GetReviewByIdQueryHandler",
    "ListGlobalReviewsQuery",
    "ListGlobalReviewsQueryHandler",
    "ListReviewsByCompanyCandidateQuery",
    "ListReviewsByCompanyCandidateQueryHandler",
    "ListReviewsByStageQuery",
    "ListReviewsByStageQueryHandler",
    # Commands
    "CreateCandidateReviewCommand",
    "CreateCandidateReviewCommandHandler",
    "DeleteCandidateReviewCommand",
    "DeleteCandidateReviewCommandHandler",
    "MarkReviewAsPendingCommand",
    "MarkReviewAsPendingCommandHandler",
    "MarkReviewAsReviewedCommand",
    "MarkReviewAsReviewedCommandHandler",
    "UpdateCandidateReviewCommand",
    "UpdateCandidateReviewCommandHandler",
]

