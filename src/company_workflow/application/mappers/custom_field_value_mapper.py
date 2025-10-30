from src.company_workflow.domain.entities.custom_field_value import CustomFieldValue
from src.company_workflow.application.dtos.custom_field_value_dto import CustomFieldValueDto


class CustomFieldValueMapper:
    """Mapper for custom field value between domain and DTO"""

    @staticmethod
    def entity_to_dto(entity: CustomFieldValue) -> CustomFieldValueDto:
        """Convert domain entity to DTO"""
        return CustomFieldValueDto(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            workflow_id=str(entity.workflow_id),
            values=entity.values,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def dto_to_entity(dto: CustomFieldValueDto) -> CustomFieldValue:
        """Convert DTO to domain entity"""
        from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
        from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
        from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId

        return CustomFieldValue(
            id=CustomFieldValueId(dto.id),
            company_candidate_id=CompanyCandidateId(dto.company_candidate_id),
            workflow_id=CompanyWorkflowId(dto.workflow_id),
            values=dto.values,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
