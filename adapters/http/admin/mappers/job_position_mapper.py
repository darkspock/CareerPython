"""Job position mapper for converting DTOs to response schemas"""
from typing import Optional, Dict, Any

from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.job_position.application.dtos.job_position_workflow_dto import JobPositionWorkflowDto
from adapters.http.admin.schemas.job_position import JobPositionResponse, JobPositionPublicResponse


class JobPositionMapper:
    """Mapper for converting JobPosition DTOs to response schemas"""

    @staticmethod
    def dto_to_response(dto: JobPositionDto, company_name: Optional[str] = None) -> JobPositionResponse:
        """Convert JobPositionDto to JobPositionResponse"""
        return JobPositionResponse.from_dto(dto, company_name=company_name)

    @staticmethod
    def get_visible_fields_for_candidate(
        dto: JobPositionDto,
        workflow_dto: Optional[JobPositionWorkflowDto] = None
    ) -> Dict[str, Any]:
        """
        Get only fields visible to candidates based on workflow/stage configuration.
        
        Args:
            dto: JobPositionDto
            workflow_dto: Optional workflow DTO (if available)
            
        Returns:
            Dict[str, Any]: Filtered custom fields visible to candidates
        """
        if not workflow_dto or not dto.stage_id:
            # If no workflow or stage, return empty dict (or all fields if no config)
            # For now, return empty dict as conservative default
            return {}
        
        # Find the current stage
        current_stage = None
        for stage in workflow_dto.stages:
            if stage.id == dto.stage_id:
                current_stage = stage
                break
        
        if not current_stage:
            # Stage not found, return empty dict
            return {}
        
        # Get default visibility from workflow config
        default_visibility = workflow_dto.custom_fields_config.get("field_candidate_visibility_default", {}) if workflow_dto.custom_fields_config else {}
        
        # Get stage-specific visibility
        stage_visibility = current_stage.field_candidate_visibility if hasattr(current_stage, 'field_candidate_visibility') else {}
        
        # Filter custom_fields_values
        visible_fields = {}
        for field_name, field_value in dto.custom_fields_values.items():
            is_visible = False
            
            # First check stage-specific visibility
            if field_name in stage_visibility:
                is_visible = stage_visibility[field_name]
            # Then check default visibility
            elif field_name in default_visibility:
                is_visible = default_visibility[field_name]
            # Default to False if not specified
            else:
                is_visible = False
            
            if is_visible:
                visible_fields[field_name] = field_value
        
        return visible_fields

    @staticmethod
    def dto_to_public_response(
        dto: JobPositionDto,
        workflow_dto: Optional[JobPositionWorkflowDto] = None,
        company_name: Optional[str] = None
    ) -> JobPositionPublicResponse:
        """Convert JobPositionDto to JobPositionPublicResponse - only visible fields for candidates"""
        visible_fields = JobPositionMapper.get_visible_fields_for_candidate(dto, workflow_dto)
        
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
