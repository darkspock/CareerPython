"""Job position admin controller"""
import logging
from decimal import Decimal
from typing import List, Optional, Dict, Any

from adapters.http.admin_app.mappers.job_position_mapper import JobPositionMapper
from adapters.http.admin_app.schemas.job_position import (
    JobPositionCreate, JobPositionUpdate, JobPositionResponse, JobPositionListResponse,
    JobPositionStatsResponse, JobPositionActionResponse
)
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.application import UpdateJobPositionCommand
# Job position commands
from src.company_bc.job_position.application.commands.create_job_position import CreateJobPositionCommand
from src.company_bc.job_position.application.commands.delete_job_position import DeleteJobPositionCommand
# Status management commands have been removed - use MoveJobPositionToStageCommand instead
from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
from src.company_bc.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQuery
from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
# Job position queries
from src.company_bc.job_position.application.queries.list_job_positions import ListJobPositionsQuery
# Domain enums
from src.company_bc.job_position.domain.enums import (
    JobPositionVisibilityEnum,
    EmploymentTypeEnum,
    ExperienceLevelEnum,
    WorkLocationTypeEnum,
    SalaryPeriodEnum,
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import (
    ListStagesByWorkflowQuery
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId

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
            page_size: Optional[int] = None,
            current_user_id: Optional[str] = None
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
                offset=offset,
                current_user_id=current_user_id
            )

            positions: List[JobPositionDto] = self.query_bus.query(query)

            # Get total count using the same filters
            # We need to get the repository from the query handler
            # For now, we'll use a simple approach: if we got fewer results than page_size,
            # that's the total. Otherwise, we estimate.
            # TODO: Add count_by_filters to the query handler or return total from query
            if len(positions) < page_size:
                # This is likely the last page or the only page
                total = (page - 1) * page_size + len(positions)
            else:
                # There might be more pages, estimate at least this many
                total = page * page_size + 1

            # Convert DTOs to response schemas using mapper
            # TODO: Ideally we should get company names in batch for performance
            response_positions = []
            for dto in positions:
                # For now, we don't have company name, could be improved by joining in query
                response_positions.append(JobPositionMapper.dto_to_response(dto, company_name=None))

            # Calculate pagination
            total_pages = (total + page_size - 1) // page_size if total > 0 else 1

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
                visibility = JobPositionVisibilityEnum(
                    position_data.visibility.lower()) if position_data.visibility else JobPositionVisibilityEnum.HIDDEN
            except (ValueError, AttributeError):
                # Fallback to default if invalid value
                visibility = JobPositionVisibilityEnum.HIDDEN

            # Convert job_category string to enum
            job_category = JobCategoryEnum(
                position_data.job_category) if position_data.job_category else JobCategoryEnum.OTHER

            # Convert workflow and stage IDs to Value Objects
            job_position_workflow_id = None
            if position_data.job_position_workflow_id:
                job_position_workflow_id = JobPositionWorkflowId.from_string(position_data.job_position_workflow_id)

            stage_id = None
            if position_data.stage_id:
                stage_id = StageId.from_string(position_data.stage_id)
            elif job_position_workflow_id:
                # If no stage_id provided but workflow is, get the first stage of the workflow
                try:
                    stages_query = ListStagesByWorkflowQuery(
                        workflow_id=WorkflowId.from_string(job_position_workflow_id.value)
                    )
                    stages: List[Any] = self.query_bus.query(stages_query)
                    if stages:
                        # Stages are ordered by position, get the first one
                        first_stage = min(stages, key=lambda s: s.order)
                        stage_id = StageId.from_string(first_stage.id)
                        logger.info(f"Auto-assigned first stage {first_stage.id} for workflow {job_position_workflow_id.value}")
                except Exception as e:
                    logger.warning(f"Could not auto-assign first stage for workflow: {e}")

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

            # Convert enum strings to enums
            employment_type = None
            if position_data.employment_type:
                try:
                    employment_type = EmploymentTypeEnum(position_data.employment_type)
                except ValueError:
                    pass

            experience_level = None
            if position_data.experience_level:
                try:
                    experience_level = ExperienceLevelEnum(position_data.experience_level)
                except ValueError:
                    pass

            work_location_type = None
            if position_data.work_location_type:
                try:
                    work_location_type = WorkLocationTypeEnum(position_data.work_location_type)
                except ValueError:
                    pass

            salary_period = None
            if position_data.salary_period:
                try:
                    salary_period = SalaryPeriodEnum(position_data.salary_period)
                except ValueError:
                    pass

            # Convert custom_fields_config schemas to domain objects
            custom_fields_config = None
            if position_data.custom_fields_config is not None:
                custom_fields_config = [
                    CustomFieldDefinition(
                        field_key=cf.field_key,
                        label=cf.label,
                        field_type=cf.field_type,
                        options=cf.options,
                        is_required=cf.is_required,
                        candidate_visible=cf.candidate_visible,
                        validation_rules=cf.validation_rules,
                        sort_order=cf.sort_order,
                        is_active=cf.is_active,
                    )
                    for cf in position_data.custom_fields_config
                ]

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
                application_deadline=(
                    position_data.application_deadline
                    if position_data.application_deadline is not None
                    else current_dto.application_deadline
                ),
                visibility=visibility,
                public_slug=position_data.public_slug if position_data.public_slug is not None else current_dto.public_slug,
                screening_template_id=position_data.screening_template_id,
                # Job details fields
                skills=position_data.skills,
                department_id=position_data.department_id,
                employment_type=employment_type,
                experience_level=experience_level,
                work_location_type=work_location_type,
                office_locations=position_data.office_locations,
                remote_restrictions=position_data.remote_restrictions,
                number_of_openings=position_data.number_of_openings,
                requisition_id=position_data.requisition_id,
                # Financial fields
                salary_currency=position_data.salary_currency,
                salary_min=Decimal(str(position_data.salary_min)) if position_data.salary_min is not None else None,
                salary_max=Decimal(str(position_data.salary_max)) if position_data.salary_max is not None else None,
                salary_period=salary_period,
                show_salary=position_data.show_salary,
                budget_max=Decimal(str(position_data.budget_max)) if position_data.budget_max is not None else None,
                # Ownership fields
                hiring_manager_id=position_data.hiring_manager_id,
                recruiter_id=position_data.recruiter_id,
                # Custom fields config
                custom_fields_config=custom_fields_config,
                # Killer questions
                killer_questions=[q.model_dump() for q in position_data.killer_questions] if position_data.killer_questions else None,
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
    # Use move_position_to_stage() instead.

    def move_position_to_stage(
            self,
            position_id: str,
            stage_id: str,
            comment: Optional[str] = None,
            user_id: Optional[str] = None
    ) -> dict:
        """Move a job position to a new stage"""
        from src.company_bc.job_position.application.commands.move_job_position_to_stage import (
            MoveJobPositionToStageCommand,
            JobPositionValidationError
        )

        try:
            command = MoveJobPositionToStageCommand(
                id=JobPositionId.from_string(position_id),
                stage_id=StageId.from_string(stage_id),
                comment=comment,
                user_id=user_id
            )
            self.command_bus.dispatch(command)

            return {
                "success": True,
                "message": "Position moved to stage successfully",
                "position_id": position_id,
                "stage_id": stage_id
            }
        except JobPositionValidationError as e:
            raise e
        except Exception as e:
            logger.error(f"Error moving position {position_id} to stage {stage_id}: {str(e)}")
            raise

    def update_custom_fields(
            self,
            position_id: str,
            custom_fields_values: Dict[str, Any]
    ) -> dict:
        """Update custom fields values for a job position"""
        from src.company_bc.job_position.application.commands.update_job_position_custom_fields import (
            UpdateJobPositionCustomFieldsCommand
        )

        try:
            command = UpdateJobPositionCustomFieldsCommand(
                id=JobPositionId.from_string(position_id),
                custom_fields_values=custom_fields_values
            )
            self.command_bus.dispatch(command)

            return {
                "success": True,
                "message": "Custom fields updated successfully",
                "position_id": position_id
            }
        except Exception as e:
            logger.error(f"Error updating custom fields for position {position_id}: {str(e)}")
            raise

    # ==================== STATUS TRANSITION METHODS ====================

    def request_approval(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Request approval for a job position (DRAFT -> PENDING_APPROVAL)"""
        from src.company_bc.job_position.application.commands import (
            RequestJobPositionApprovalCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError,
            JobPositionBudgetExceededError
        )

        try:
            command = RequestJobPositionApprovalCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Approval requested successfully",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except JobPositionBudgetExceededError as e:
            logger.warning(f"Budget exceeded for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error requesting approval for position {position_id}: {str(e)}")
            raise

    def approve_position(
            self,
            position_id: str,
            approver_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Approve a job position (PENDING_APPROVAL -> APPROVED)"""
        from src.company_bc.job_position.application.commands import (
            ApproveJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = ApproveJobPositionCommand(
                job_position_id=position_id,
                approver_id=approver_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position approved successfully",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error approving position {position_id}: {str(e)}")
            raise

    def reject_position(
            self,
            position_id: str,
            company_id: str,
            reason: Optional[str] = None
    ) -> JobPositionActionResponse:
        """Reject a job position (PENDING_APPROVAL -> REJECTED)"""
        from src.company_bc.job_position.application.commands import (
            RejectJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = RejectJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id,
                reason=reason
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position rejected",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error rejecting position {position_id}: {str(e)}")
            raise

    def publish_position(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Publish a job position (APPROVED/DRAFT -> PUBLISHED)"""
        from src.company_bc.job_position.application.commands import (
            PublishJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = PublishJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position published successfully",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error publishing position {position_id}: {str(e)}")
            raise

    def hold_position(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Put a job position on hold (PUBLISHED -> ON_HOLD)"""
        from src.company_bc.job_position.application.commands import (
            HoldJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = HoldJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position put on hold",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error putting position {position_id} on hold: {str(e)}")
            raise

    def resume_position(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Resume a held job position (ON_HOLD -> PUBLISHED)"""
        from src.company_bc.job_position.application.commands import (
            ResumeJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = ResumeJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position resumed",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error resuming position {position_id}: {str(e)}")
            raise

    def close_position(
            self,
            position_id: str,
            company_id: str,
            closed_reason: str
    ) -> JobPositionActionResponse:
        """Close a job position (PUBLISHED/ON_HOLD -> CLOSED)"""
        from src.company_bc.job_position.application.commands import (
            CloseJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = CloseJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id,
                closed_reason=closed_reason
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position closed",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except ValueError as e:
            # Invalid closed_reason enum value
            logger.warning(f"Invalid closed_reason for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Invalid closed reason: {closed_reason}",
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error closing position {position_id}: {str(e)}")
            raise

    def archive_position(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Archive a job position (various -> ARCHIVED)"""
        from src.company_bc.job_position.application.commands import (
            ArchiveJobPositionCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = ArchiveJobPositionCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position archived",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error archiving position {position_id}: {str(e)}")
            raise

    def revert_to_draft(
            self,
            position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Revert a job position to draft (REJECTED/APPROVED/CLOSED -> DRAFT)"""
        from src.company_bc.job_position.application.commands import (
            RevertJobPositionToDraftCommand
        )
        from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
            JobPositionInvalidStatusTransitionError
        )

        try:
            command = RevertJobPositionToDraftCommand(
                job_position_id=position_id,
                company_id=company_id
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position reverted to draft",
                position_id=position_id
            )
        except JobPositionInvalidStatusTransitionError as e:
            logger.warning(f"Invalid status transition for position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=str(e),
                position_id=position_id
            )
        except Exception as e:
            logger.error(f"Error reverting position {position_id} to draft: {str(e)}")
            raise

    def clone_position(
            self,
            source_position_id: str,
            company_id: str
    ) -> JobPositionActionResponse:
        """Clone a job position (creates new position in DRAFT)"""
        from src.company_bc.job_position.application.commands import (
            CloneJobPositionCommand
        )

        try:
            new_position_id = JobPositionId.generate()
            command = CloneJobPositionCommand(
                source_job_position_id=source_position_id,
                company_id=company_id,
                new_job_position_id=new_position_id.value
            )
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position cloned successfully",
                position_id=new_position_id.value
            )
        except Exception as e:
            logger.error(f"Error cloning position {source_position_id}: {str(e)}")
            raise

    def create_inline_screening_template(
            self,
            position_id: str,
            company_id: str,
            name: Optional[str] = None,
            intro: Optional[str] = None,
            prompt: Optional[str] = None,
            goal: Optional[str] = None,
            created_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a screening template inline and link it to a job position"""
        from adapters.http.admin_app.schemas.job_position import CreateInlineScreeningTemplateResponse
        from src.company_bc.job_position.application.commands.create_inline_screening_template import (
            CreateInlineScreeningTemplateCommand
        )

        try:
            command = CreateInlineScreeningTemplateCommand(
                position_id=JobPositionId.from_string(position_id),
                company_id=CompanyId.from_string(company_id),
                name=name,
                intro=intro,
                prompt=prompt,
                goal=goal,
                created_by=created_by
            )
            self.command_bus.dispatch(command)

            # Get the updated position to retrieve the template ID
            position = self.get_position_by_id(position_id)

            return CreateInlineScreeningTemplateResponse(
                success=True,
                message="Screening template created and linked successfully",
                template_id=position.screening_template_id,
                position_id=position_id
            ).model_dump()
        except Exception as e:
            logger.error(f"Error creating inline screening template for position {position_id}: {str(e)}")
            raise
