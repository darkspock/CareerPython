"""Position stage assignment module"""
from adapters.http.candidate_app.schemas.position_stage_assignment_schemas import AssignUsersToStageRequest, \
    AddUserToStageRequest, RemoveUserFromStageRequest, CopyWorkflowAssignmentsRequest, PositionStageAssignmentResponse
from adapters.http.company_app.position_stage_assignment.mappers import PositionStageAssignmentMapper
from .application import (
    AssignUsersToStageCommand,
    AssignUsersToStageCommandHandler,
    AddUserToStageCommand,
    AddUserToStageCommandHandler,
    RemoveUserFromStageCommand,
    RemoveUserFromStageCommandHandler,
    CopyWorkflowAssignmentsCommand,
    CopyWorkflowAssignmentsCommandHandler,
    WorkflowStageAssignment,
    PositionStageAssignmentDto,
    ListStageAssignmentsQuery,
    ListStageAssignmentsQueryHandler,
    GetAssignedUsersQuery,
    GetAssignedUsersQueryHandler
)
from .domain import (
    PositionStageAssignment,
    PositionStageAssignmentId,
    PositionStageAssignmentRepositoryInterface,
    PositionStageAssignmentException,
    PositionStageAssignmentNotFoundException,
    PositionStageAssignmentValidationError,
    DuplicatePositionStageAssignmentException
)
from .infrastructure import (
    PositionStageAssignmentModel,
    PositionStageAssignmentRepository
)

__all__ = [
    # Application
    'AssignUsersToStageCommand',
    'AssignUsersToStageCommandHandler',
    'AddUserToStageCommand',
    'AddUserToStageCommandHandler',
    'RemoveUserFromStageCommand',
    'RemoveUserFromStageCommandHandler',
    'CopyWorkflowAssignmentsCommand',
    'CopyWorkflowAssignmentsCommandHandler',
    'WorkflowStageAssignment',
    'PositionStageAssignmentDto',
    'ListStageAssignmentsQuery',
    'ListStageAssignmentsQueryHandler',
    'GetAssignedUsersQuery',
    'GetAssignedUsersQueryHandler',
    # Domain
    'PositionStageAssignment',
    'PositionStageAssignmentId',
    'PositionStageAssignmentRepositoryInterface',
    'PositionStageAssignmentException',
    'PositionStageAssignmentNotFoundException',
    'PositionStageAssignmentValidationError',
    'DuplicatePositionStageAssignmentException',
    # Infrastructure
    'PositionStageAssignmentModel',
    'PositionStageAssignmentRepository',
    # Presentation
    'AssignUsersToStageRequest',
    'AddUserToStageRequest',
    'RemoveUserFromStageRequest',
    'CopyWorkflowAssignmentsRequest',
    'PositionStageAssignmentResponse',
    'PositionStageAssignmentMapper'
]
