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
            required_outcome=dto.required_outcome,
            estimated_duration_days=dto.estimated_duration_days,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
