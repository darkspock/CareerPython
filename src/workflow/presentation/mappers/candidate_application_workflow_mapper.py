from src.workflow.application.dtos.workflow_dto import WorkflowDto
from src.workflow.presentation.schemas.candidate_application_workflow_response import WorkflowResponse


class WorkflowResponseMapper:
    """Mapper for converting WorkflowDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: WorkflowDto) -> WorkflowResponse:
        """Convert DTO to response"""
        return WorkflowResponse(
            id=dto.id,
            company_id=dto.company_id,
            phase_id=dto.phase_id,
            name=dto.name,
            description=dto.description,
            status=dto.status,
            is_default=dto.is_default,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
