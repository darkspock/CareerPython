"""Phase mapper for converting DTOs to response schemas"""
from adapters.http.shared.phase.schemas.phase_schemas import PhaseResponse
from src.shared_bc.customization.phase.application.queries.get_phase_by_id_query import PhaseDto


class PhaseMapper:
    """Mapper for converting Phase DTOs to Response schemas"""

    @staticmethod
    def dto_to_response(dto: PhaseDto) -> PhaseResponse:
        """Convert PhaseDto to PhaseResponse

        Args:
            dto: PhaseDto from query handler

        Returns:
            PhaseResponse for API response
        """
        return PhaseResponse(
            id=dto.id,
            company_id=dto.company_id,
            workflow_type=dto.workflow_type,
            name=dto.name,
            sort_order=dto.sort_order,
            default_view=dto.default_view,
            status=dto.status,
            objective=dto.objective,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
