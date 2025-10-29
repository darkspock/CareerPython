from src.company_workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.company_workflow.presentation.schemas.workflow_stage_response import WorkflowStageResponse


class WorkflowStageResponseMapper:
    """Mapper for converting WorkflowStageDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: WorkflowStageDto) -> WorkflowStageResponse:
        """Convert DTO to response"""
        return WorkflowStageResponse(
            id=dto.id,
            workflow_id=dto.workflow_id,
            name=dto.name,
            description=dto.description,
            stage_type=dto.stage_type,
            order=dto.order,
            allow_skip=dto.allow_skip,
            estimated_duration_days=dto.estimated_duration_days,
            is_active=dto.is_active,
            default_role_ids=dto.default_role_ids,
            default_assigned_users=dto.default_assigned_users,
            email_template_id=dto.email_template_id,
            custom_email_text=dto.custom_email_text,
            deadline_days=dto.deadline_days,
            estimated_cost=dto.estimated_cost,
            next_phase_id=dto.next_phase_id,
            kanban_display=dto.kanban_display,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
