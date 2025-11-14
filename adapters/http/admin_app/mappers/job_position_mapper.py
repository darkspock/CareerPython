"""Job position mapper for converting DTOs to response schemas"""
from typing import Optional, Dict, Any, List

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from adapters.http.admin_app.schemas.job_position import JobPositionResponse, JobPositionPublicResponse
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto


class JobPositionMapper:
    """Mapper for converting JobPosition DTOs to response schemas"""

    @staticmethod
    def dto_to_response(dto: JobPositionDto, company_name: Optional[str] = None) -> JobPositionResponse:
        """Convert JobPositionDto to JobPositionResponse"""
        return JobPositionResponse.from_dto(dto, company_name=company_name)

    @staticmethod
    def get_visible_fields_for_candidate(
        dto: JobPositionDto,
        workflow_dto: Optional[WorkflowDto] = None,
        stages: Optional[List[WorkflowStageDto]] = None
    ) -> Dict[str, Any]:
        """
        Get only fields visible to candidates based on workflow/stage configuration.
        
        Note: Field visibility is now managed through the EntityCustomization system.
        This method returns all custom fields for now, as visibility is handled
        at the customization level.
        
        Args:
            dto: JobPositionDto
            workflow_dto: Optional workflow DTO (if available)
            stages: Optional list of workflow stages (if available)
            
        Returns:
            Dict[str, Any]: Filtered custom fields visible to candidates
        """
        # For now, return all custom fields as visibility is managed through
        # the EntityCustomization system. This can be enhanced later to filter
        # based on stage-specific visibility rules if needed.
        return dto.custom_fields_values or {}

    @staticmethod
    def dto_to_public_response(
        dto: JobPositionDto,
        workflow_dto: Optional[WorkflowDto] = None,
        stages: Optional[List[WorkflowStageDto]] = None,
        company_name: Optional[str] = None
    ) -> JobPositionPublicResponse:
        """Convert JobPositionDto to JobPositionPublicResponse - only visible fields for candidates"""
        visible_fields = JobPositionMapper.get_visible_fields_for_candidate(dto, workflow_dto, stages)
        
        return JobPositionPublicResponse(
            id=dto.id.value,
            title=dto.title,
            company_id=dto.company_id.value,
            description=dto.description,
            job_category=dto.job_category.value,
            open_at=dto.open_at,
            application_deadline=dto.application_deadline,
            public_slug=dto.public_slug,
            visible_fields=visible_fields,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def _contract_type_to_employment_type(contract_type: str) -> str:
        """Map contract type to employment type"""
        mapping = {
            "full_time": "full_time",
            "part_time": "part_time",
            "contract": "contract",
            "internship": "internship"
        }
        return mapping.get(contract_type, "full_time")

    @staticmethod
    def _position_level_to_experience_level(position_level: Optional[str]) -> Optional[str]:
        """Map position level to experience level"""
        if not position_level:
            return None

        mapping = {
            "junior": "junior",
            "mid": "mid",
            "senior": "senior",
            "lead": "lead"
        }
        return mapping.get(position_level.lower())
