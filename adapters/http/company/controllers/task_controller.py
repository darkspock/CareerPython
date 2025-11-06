"""
Task Controller for managing task assignment and processing
Phase 6: Task Management System
"""
import logging
from typing import List, Optional

from fastapi import HTTPException

from src.candidate_application.application.commands.claim_task_command import ClaimTaskCommand
from src.candidate_application.application.commands.unclaim_task_command import UnclaimTaskCommand
from src.candidate_application.application.queries.get_my_assigned_tasks_query import GetMyAssignedTasksQuery
from src.candidate_application.application.queries.shared.candidate_application_dto import CandidateApplicationDto
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus

logger = logging.getLogger(__name__)


class TaskController:
    """Controller for managing task assignment and processing"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def get_my_assigned_tasks(
            self,
            user_id: str,
            stage_id: Optional[str] = None,
            limit: Optional[int] = None
    ) -> List[CandidateApplicationDto]:
        """Get all tasks assigned to the current user

        Args:
            user_id: ID of the user requesting tasks
            stage_id: Optional filter by specific stage
            limit: Optional limit on number of results

        Returns:
            List of applications assigned to the user, sorted by priority
        """
        try:
            query = GetMyAssignedTasksQuery(
                user_id=user_id,
                stage_id=stage_id,
                limit=limit
            )

            applications: List[CandidateApplicationDto] = self._query_bus.query(query)
            return applications

        except Exception as e:
            logger.error(f"Error getting assigned tasks for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving assigned tasks: {str(e)}")

    def claim_task(
            self,
            application_id: str,
            user_id: str
    ) -> dict:
        """Claim a task for processing

        Args:
            application_id: ID of the application to claim
            user_id: ID of the user claiming the task

        Returns:
            Success message
        """
        try:
            command = ClaimTaskCommand(
                application_id=application_id,
                user_id=user_id
            )

            self._command_bus.execute(command)

            return {
                "message": "Task claimed successfully",
                "application_id": application_id,
                "user_id": user_id
            }

        except ValueError as e:
            logger.warning(f"Invalid claim task request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error claiming task {application_id} for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error claiming task: {str(e)}")

    def unclaim_task(
            self,
            application_id: str,
            user_id: str
    ) -> dict:
        """Unclaim/release a task back to pending status

        Args:
            application_id: ID of the application to unclaim
            user_id: ID of the user unclaiming the task

        Returns:
            Success message
        """
        try:
            command = UnclaimTaskCommand(
                application_id=application_id,
                user_id=user_id
            )

            self._command_bus.execute(command)

            return {
                "message": "Task unclaimed successfully",
                "application_id": application_id,
                "user_id": user_id
            }

        except ValueError as e:
            logger.warning(f"Invalid unclaim task request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error unclaiming task {application_id} for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error unclaiming task: {str(e)}")
