from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.domain.entities.company_workflow import CompanyWorkflow


class CompanyWorkflowMapper:
    """Mapper for converting CompanyWorkflow entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CompanyWorkflow) -> CompanyWorkflowDto:
        """Convert entity to DTO"""
        return CompanyWorkflowDto(
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
