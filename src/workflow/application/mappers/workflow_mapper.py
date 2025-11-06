from src.workflow.application.dtos.workflow_dto import WorkflowDto
from src.workflow.domain.entities.workflow import Workflow


class WorkflowMapper:
    """Mapper for converting Workflow entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: Workflow) -> WorkflowDto:
        """Convert entity to DTO"""
        return WorkflowDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            workflow_type=entity.workflow_type.value,
            display=entity.display.value,
            phase_id=str(entity.phase_id) if entity.phase_id else None,
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
