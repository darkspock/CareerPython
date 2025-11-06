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
            phase_id=entity.phase_id,
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
