from typing import Optional, Dict, Any

from adapters.http.company_app.company_candidate.schemas.company_candidate_response import CompanyCandidateResponse
from src.company_bc.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_bc.company_candidate.domain.read_models.company_candidate_with_candidate_read_model import (
    CompanyCandidateWithCandidateReadModel
)


class CompanyCandidateResponseMapper:
    """Mapper for converting CompanyCandidateDto and ReadModels to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyCandidateDto) -> CompanyCandidateResponse:
        """Convert DTO to response"""
        return CompanyCandidateResponse(
            id=dto.id,
            company_id=dto.company_id,
            candidate_id=dto.candidate_id,
            status=dto.status,
            ownership_status=dto.ownership_status,
            created_by_user_id=dto.created_by_user_id,
            workflow_id=dto.workflow_id,
            current_stage_id=dto.current_stage_id,
            phase_id=dto.phase_id,
            invited_at=dto.invited_at,
            confirmed_at=dto.confirmed_at,
            rejected_at=dto.rejected_at,
            archived_at=dto.archived_at,
            visibility_settings=dto.visibility_settings,
            tags=dto.tags,
            position=dto.position,
            department=dto.department,
            priority=dto.priority,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    @staticmethod
    def read_model_to_response(
            read_model: CompanyCandidateWithCandidateReadModel,
            custom_field_values: Optional[Dict[str, Any]] = None
    ) -> CompanyCandidateResponse:
        """Convert ReadModel to response"""
        return CompanyCandidateResponse(
            id=read_model.id,
            company_id=read_model.company_id,
            candidate_id=read_model.candidate_id,
            status=read_model.status,
            ownership_status=read_model.ownership_status,
            created_by_user_id=read_model.created_by_user_id,
            workflow_id=read_model.workflow_id,
            current_stage_id=read_model.current_stage_id,
            phase_id=read_model.phase_id,
            invited_at=read_model.invited_at,
            confirmed_at=read_model.confirmed_at,
            rejected_at=read_model.rejected_at,
            archived_at=read_model.archived_at,
            visibility_settings=read_model.visibility_settings,
            tags=read_model.tags,
            position=read_model.position,
            department=read_model.department,
            priority=read_model.priority,
            created_at=read_model.created_at,
            updated_at=read_model.updated_at,
            # Include candidate info from read model
            candidate_name=read_model.candidate_name,
            candidate_email=read_model.candidate_email,
            candidate_phone=read_model.candidate_phone,
            # Include job position info from read model
            job_position_id=read_model.job_position_id,
            job_position_title=read_model.job_position_title,
            application_status=read_model.application_status,
            # Include workflow and stage info from read model
            stage_name=read_model.stage_name,
            workflow_name=read_model.workflow_name,
            stage_style=read_model.stage_style,
            # Include phase info from read model
            phase_name=read_model.phase_name,
            # Include custom field values if provided
            custom_field_values=custom_field_values,
            # Include comment counts from read model
            pending_comments_count=read_model.pending_comments_count,
        )
