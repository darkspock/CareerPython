"""Mapper for position stage assignment DTO to response schema"""
from typing import List

from src.position_stage_assignment.application import PositionStageAssignmentDto
from src.position_stage_assignment.presentation.schemas import PositionStageAssignmentResponse


class PositionStageAssignmentMapper:
    """Mapper for position stage assignment"""

    @staticmethod
    def dto_to_response(dto: PositionStageAssignmentDto) -> PositionStageAssignmentResponse:
        """Convert DTO to response schema"""
        return PositionStageAssignmentResponse(
            id=dto.id,
            position_id=dto.position_id,
            stage_id=dto.stage_id,
            assigned_user_ids=dto.assigned_user_ids,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def dto_list_to_response_list(dtos: List[PositionStageAssignmentDto]) -> List[PositionStageAssignmentResponse]:
        """Convert list of DTOs to list of response schemas"""
        return [PositionStageAssignmentMapper.dto_to_response(dto) for dto in dtos]
