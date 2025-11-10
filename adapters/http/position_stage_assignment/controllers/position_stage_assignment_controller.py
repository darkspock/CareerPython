"""Position stage assignment controller"""
from typing import List

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.company_bc.position_stage_assignment import (
    AssignUsersToStageCommand,
    AddUserToStageCommand,
    RemoveUserFromStageCommand,
    CopyWorkflowAssignmentsCommand,
    ListStageAssignmentsQuery,
    GetAssignedUsersQuery,
    WorkflowStageAssignment
)
from src.company_bc.position_stage_assignment.presentation.schemas import (
    AssignUsersToStageRequest,
    AddUserToStageRequest,
    RemoveUserFromStageRequest,
    CopyWorkflowAssignmentsRequest,
    PositionStageAssignmentResponse
)
from src.company_bc.position_stage_assignment import PositionStageAssignmentMapper


class PositionStageAssignmentController:
    """Controller for position stage assignment operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def assign_users_to_stage(self, request: AssignUsersToStageRequest) -> PositionStageAssignmentResponse:
        """Assign users to a stage"""
        command = AssignUsersToStageCommand(
            position_id=request.position_id,
            stage_id=request.stage_id,
            user_ids=request.user_ids
        )
        self.command_bus.execute(command)

        # Get full assignment details
        list_query = ListStageAssignmentsQuery(position_id=request.position_id)
        from src.company_bc.position_stage_assignment import PositionStageAssignmentDto
        assignments: List[PositionStageAssignmentDto] = self.query_bus.query(list_query)

        # Find the specific assignment
        assignment = next(
            (a for a in assignments if a.stage_id == request.stage_id),
            None
        )

        if assignment:
            return PositionStageAssignmentMapper.dto_to_response(assignment)

        # This should not happen, but handle gracefully
        raise ValueError(f"Assignment not found for position {request.position_id} and stage {request.stage_id}")

    def add_user_to_stage(self, request: AddUserToStageRequest) -> PositionStageAssignmentResponse:
        """Add a user to a stage"""
        command = AddUserToStageCommand(
            position_id=request.position_id,
            stage_id=request.stage_id,
            user_id=request.user_id
        )
        self.command_bus.execute(command)

        # Query the updated assignment
        list_query = ListStageAssignmentsQuery(position_id=request.position_id)
        from src.company_bc.position_stage_assignment import PositionStageAssignmentDto
        assignments: List[PositionStageAssignmentDto] = self.query_bus.query(list_query)

        assignment = next(
            (a for a in assignments if a.stage_id == request.stage_id),
            None
        )

        if assignment:
            return PositionStageAssignmentMapper.dto_to_response(assignment)

        raise ValueError(f"Assignment not found for position {request.position_id} and stage {request.stage_id}")

    def remove_user_from_stage(self, request: RemoveUserFromStageRequest) -> PositionStageAssignmentResponse:
        """Remove a user from a stage"""
        command = RemoveUserFromStageCommand(
            position_id=request.position_id,
            stage_id=request.stage_id,
            user_id=request.user_id
        )
        self.command_bus.execute(command)

        # Query the updated assignment
        list_query = ListStageAssignmentsQuery(position_id=request.position_id)
        from src.company_bc.position_stage_assignment import PositionStageAssignmentDto
        assignments: List[PositionStageAssignmentDto] = self.query_bus.query(list_query)

        assignment = next(
            (a for a in assignments if a.stage_id == request.stage_id),
            None
        )

        if assignment:
            return PositionStageAssignmentMapper.dto_to_response(assignment)

        raise ValueError(f"Assignment not found for position {request.position_id} and stage {request.stage_id}")

    def copy_workflow_assignments(self, request: CopyWorkflowAssignmentsRequest) -> List[PositionStageAssignmentResponse]:
        """Copy workflow assignments to a position"""
        workflow_stages = [
            WorkflowStageAssignment(
                stage_id=wa.stage_id,
                default_user_ids=wa.default_user_ids
            )
            for wa in request.workflow_assignments
        ]

        command = CopyWorkflowAssignmentsCommand(
            position_id=request.position_id,
            workflow_stages=workflow_stages
        )
        self.command_bus.execute(command)

        # Query all assignments for the position
        query = ListStageAssignmentsQuery(position_id=request.position_id)
        from src.company_bc.position_stage_assignment import PositionStageAssignmentDto
        assignments: List[PositionStageAssignmentDto] = self.query_bus.query(query)

        return PositionStageAssignmentMapper.dto_list_to_response_list(assignments)

    def list_stage_assignments(self, position_id: str) -> List[PositionStageAssignmentResponse]:
        """List all stage assignments for a position"""
        query = ListStageAssignmentsQuery(position_id=position_id)
        from src.company_bc.position_stage_assignment import PositionStageAssignmentDto
        assignments: List[PositionStageAssignmentDto] = self.query_bus.query(query)
        return PositionStageAssignmentMapper.dto_list_to_response_list(assignments)

    def get_assigned_users(self, position_id: str, stage_id: str) -> List[str]:
        """Get assigned users for a specific position-stage combination"""
        query = GetAssignedUsersQuery(
            position_id=position_id,
            stage_id=stage_id
        )
        return self.query_bus.query(query)
