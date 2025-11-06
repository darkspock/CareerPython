from src.customization.application.custom_field_value_dto import CustomFieldValueDto
from src.customization.custom_field_value_response import CustomFieldValueResponse


class CustomFieldValueResponseMapper:
    """Mapper for custom field value between DTO and response"""

    @staticmethod
    def dto_to_response(dto: CustomFieldValueDto) -> CustomFieldValueResponse:
        """Convert DTO to response"""
        return CustomFieldValueResponse(
            id=dto.id,
            company_candidate_id=dto.company_candidate_id,
            workflow_id=dto.workflow_id,
            values=dto.values,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
