from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.workflow.domain.entities.workflow_stage import WorkflowStage


class WorkflowStageMapper:
    """Mapper for converting WorkflowStage entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: WorkflowStage) -> WorkflowStageDto:
        """Convert entity to DTO"""
        return WorkflowStageDto(
            id=str(entity.id),
            workflow_id=str(entity.workflow_id),
            name=entity.name,
            description=entity.description,
            stage_type=entity.stage_type.value,
            order=entity.order,
            allow_skip=entity.allow_skip,
            estimated_duration_days=entity.estimated_duration_days,
            is_active=entity.is_active,
            default_role_ids=entity.default_role_ids,
            default_assigned_users=entity.default_assigned_users,
            email_template_id=entity.email_template_id,
            custom_email_text=entity.custom_email_text,
            deadline_days=entity.deadline_days,
            estimated_cost=entity.estimated_cost,
            next_phase_id=str(entity.next_phase_id) if entity.next_phase_id else None,
            kanban_display=entity.kanban_display.value,
            style={
                "background_color": entity.style.background_color,
                "text_color": entity.style.text_color,
                "icon": entity.style.icon
            },
            validation_rules=entity.validation_rules,
            recommended_rules=entity.recommended_rules,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
