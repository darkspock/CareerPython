"""Job position admin controller"""
import logging
from datetime import date
from typing import List, Optional, Dict, Any

from adapters.http.admin.mappers.job_position_mapper import JobPositionMapper
from adapters.http.admin.schemas.job_position import (
    JobPositionCreate, JobPositionUpdate, JobPositionResponse, JobPositionListResponse,
    JobPositionStatsResponse, JobPositionActionResponse
)
from src.company.domain.value_objects.company_id import CompanyId
# Job position commands
from src.job_position.application.commands.create_job_position import CreateJobPositionCommand
from src.job_position.application.commands.delete_job_position import DeleteJobPositionCommand
from src.job_position.application.commands.update_job_position import UpdateJobPositionCommand
# Status management commands have been removed - use MoveJobPositionToStageCommand instead
from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
from src.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQuery
from src.job_position.application.queries.job_position_dto import JobPositionDto
# Job position queries
from src.job_position.application.queries.list_job_positions import ListJobPositionsQuery
# Domain enums
from src.job_position.domain.enums import JobPositionVisibilityEnum
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.shared.domain.enums.job_category import JobCategoryEnum

# DTOs and schemas

logger = logging.getLogger(__name__)


class JobPositionController:
    """Controller for job position admin operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def list_positions(
            self,
            company_id: Optional[str] = None,
            search_term: Optional[str] = None,
            department: Optional[str] = None,
            location: Optional[str] = None,
            employment_type: Optional[str] = None,
            experience_level: Optional[str] = None,
            is_remote: Optional[bool] = None,
            is_active: Optional[bool] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> JobPositionListResponse:
        """List job positions with filters"""
        try:
            page = page or 1
            page_size = page_size or 10
            offset = (page - 1) * page_size

            query = ListJobPositionsQuery(
                company_id=company_id,
                search_term=search_term,
                limit=page_size,
                offset=offset
            )

            positions: List[JobPositionDto] = self.query_bus.query(query)

            # Convert DTOs to response schemas using mapper
            # TODO: Ideally we should get company names in batch for performance
            response_positions = []
            for dto in positions:
                # For now, we don't have company name, could be improved by joining in query
                response_positions.append(JobPositionMapper.dto_to_response(dto, company_name=None))

            # Calculate pagination
            total = len(response_positions)  # This is simplified, should be from repository
            total_pages = (total + page_size - 1) // page_size

            return JobPositionListResponse(
                positions=response_positions,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )

        except Exception as e:
            logger.error(f"Error listing positions: {str(e)}")
            raise

    def get_position_stats(self) -> JobPositionStatsResponse:
        """Get job position statistics"""
        try:
            query = GetJobPositionsStatsQuery()
            stats_data: Dict[str, Any] = self.query_bus.query(query)

            return JobPositionStatsResponse(
                total_positions=stats_data.get("total_count", 0),
                active_positions=stats_data.get("active_count", 0),
                inactive_positions=stats_data.get("inactive_count", 0),
                positions_by_type={},
                positions_by_company={}
            )

        except Exception as e:
            logger.error(f"Error getting position stats: {str(e)}")
            raise

    def get_position_by_id(self, position_id: str) -> JobPositionResponse:
        """Get a specific job position by ID"""
        try:
            query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
            position_dto: Optional[JobPositionDto] = self.query_bus.query(query)

            if not position_dto:
                raise ValueError(f"Position with ID {position_id} not found")

            # TODO: Could fetch company name for better UX
            return JobPositionMapper.dto_to_response(position_dto, company_name=None)

        except Exception as e:
            logger.error(f"Error getting position {position_id}: {str(e)}")
            raise

    def create_position(self, position_data: JobPositionCreate) -> JobPositionActionResponse:
        """Create a new job position - simplified"""
        try:
            # Convert visibility string to enum (already normalized to lowercase by validator)
            try:
                visibility = JobPositionVisibilityEnum(position_data.visibility.lower()) if position_data.visibility else JobPositionVisibilityEnum.HIDDEN
            except (ValueError, AttributeError):
                # Fallback to default if invalid value
                visibility = JobPositionVisibilityEnum.HIDDEN
            
            # Convert job_category string to enum
            job_category = JobCategoryEnum(position_data.job_category) if position_data.job_category else JobCategoryEnum.OTHER
            
            # Convert workflow and stage IDs to Value Objects
            job_position_workflow_id = None
            if position_data.job_position_workflow_id:
                job_position_workflow_id = JobPositionWorkflowId.from_string(position_data.job_position_workflow_id)
            
            stage_id = None
            if position_data.stage_id:
                stage_id = StageId.from_string(position_data.stage_id)

            id = JobPositionId.generate()
            command = CreateJobPositionCommand(
                id=id,
                company_id=CompanyId.from_string(position_data.company_id),
                job_position_workflow_id=job_position_workflow_id,
                stage_id=stage_id,
                phase_workflows=position_data.phase_workflows,
                custom_fields_values=position_data.custom_fields_values or {},
                title=position_data.title,
                description=position_data.description,
                job_category=job_category,
                open_at=position_data.open_at,
                application_deadline=position_data.application_deadline,
                visibility=visibility,
                public_slug=position_data.public_slug
            )

            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position created successfully",
                position_id=id.value
            )

        except ValueError as e:
            logger.error(f"Validation error creating position: {str(e)}")
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating position: {str(e)}")
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"Failed to create position: {str(e)}")

    def update_position(self, position_id: str, position_data: JobPositionUpdate) -> JobPositionActionResponse:
        """Update an existing job position - simplified"""
        try:
            # Get current position to preserve values not provided
            current_position_query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
            current_dto: Optional[JobPositionDto] = self.query_bus.query(current_position_query)

            if not current_dto:
                return JobPositionActionResponse(
                    success=False,
                    message=f"Position with ID {position_id} not found",
                    position_id=position_id
                )

            # Convert visibility string to enum if provided (already normalized to lowercase by validator)
            visibility = None
            if position_data.visibility:
                try:
                    visibility = JobPositionVisibilityEnum(position_data.visibility.lower())
                except (ValueError, AttributeError):
                    pass  # Keep current value if invalid

            # Convert job_category string to enum if provided
            job_category = None
            if position_data.job_category:
                try:
                    job_category = JobCategoryEnum(position_data.job_category)
                except ValueError:
                    pass  # Keep current value if invalid

            # Convert workflow and stage IDs to Value Objects if provided
            job_position_workflow_id = None
            if position_data.job_position_workflow_id:
                job_position_workflow_id = JobPositionWorkflowId.from_string(position_data.job_position_workflow_id)
            elif current_dto.job_position_workflow_id:
                job_position_workflow_id = JobPositionWorkflowId.from_string(current_dto.job_position_workflow_id)

            stage_id = None
            if position_data.stage_id:
                stage_id = StageId.from_string(position_data.stage_id)
            elif current_dto.stage_id:
                stage_id = StageId.from_string(current_dto.stage_id)

            # Merge custom_fields_values if provided
            custom_fields_values = position_data.custom_fields_values
            if custom_fields_values and current_dto.custom_fields_values:
                # Merge new values into existing
                merged = current_dto.custom_fields_values.copy()
                merged.update(custom_fields_values)
                custom_fields_values = merged
            elif not custom_fields_values:
                custom_fields_values = current_dto.custom_fields_values

            command = UpdateJobPositionCommand(
                id=JobPositionId.from_string(position_id),
                job_position_workflow_id=job_position_workflow_id,
                stage_id=stage_id,
                phase_workflows=position_data.phase_workflows if position_data.phase_workflows is not None else current_dto.phase_workflows,
                custom_fields_values=custom_fields_values,
                title=position_data.title if position_data.title else current_dto.title,
                description=position_data.description if position_data.description is not None else current_dto.description,
                job_category=job_category,
                open_at=position_data.open_at if position_data.open_at is not None else current_dto.open_at,
                application_deadline=position_data.application_deadline if position_data.application_deadline is not None else current_dto.application_deadline,
                visibility=visibility,
                public_slug=position_data.public_slug if position_data.public_slug is not None else current_dto.public_slug
            )

            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position updated successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error updating position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to update position: {str(e)}"
            )

    def delete_position(self, position_id: str) -> JobPositionActionResponse:
        """Delete a job position"""
        try:
            command = DeleteJobPositionCommand(id=JobPositionId.from_string(position_id))
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position deleted successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error deleting position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to delete position: {str(e)}"
            )

# Status management methods (activate, pause, resume, close, archive) have been removed.
# Use JobPositionWorkflowController.move_position_to_stage() instead.
