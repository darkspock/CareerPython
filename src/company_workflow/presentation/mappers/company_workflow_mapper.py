from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.presentation.schemas.company_workflow_response import CompanyWorkflowResponse


class CompanyWorkflowResponseMapper:
    """Mapper for converting CompanyWorkflowDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyWorkflowDto) -> CompanyWorkflowResponse:
        """Convert DTO to response"""
        return CompanyWorkflowResponse(
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
