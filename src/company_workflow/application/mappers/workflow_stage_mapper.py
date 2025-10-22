from src.company_workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.company_workflow.domain.entities.workflow_stage import WorkflowStage


class WorkflowStageMapper:
    """Mapper for converting WorkflowStage entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: WorkflowStage) -> WorkflowStageDto:
        """Convert entity to DTO"""
        return WorkflowStageDto(
            id=str(entity.id),
            workflow_id=str(entity.workflow_id),
            name=entity.name,
            description=entity.description,
            stage_type=entity.stage_type.value,
            order=entity.order,
            required_outcome=entity.required_outcome.value if entity.required_outcome else None,
            estimated_duration_days=entity.estimated_duration_days,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
