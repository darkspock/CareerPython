from adapters.http.shared.workflow.schemas.workflow_response import WorkflowResponse
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto


class WorkflowResponseMapper:
    """Mapper for converting WorkflowDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: WorkflowDto) -> WorkflowResponse:
        """Convert DTO to response"""
        return WorkflowResponse(
            id=dto.id,
            company_id=dto.company_id,
            workflow_type=dto.workflow_type,
            display=dto.display,
            phase_id=dto.phase_id,
            name=dto.name,
            description=dto.description,
            status=dto.status,
            is_default=dto.is_default,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
