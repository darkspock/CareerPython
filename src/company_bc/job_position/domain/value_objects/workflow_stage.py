from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_bc.job_position.domain.enums.kanban_display import KanbanDisplayEnum
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum


@dataclass(frozen=True)
class WorkflowStage:
    """
    Value object representing a stage in a JobPosition workflow.
    
    This is a simplified version for JobPosition workflows, different from
    the candidate workflow stages.
    """
    id: StageId
    name: str
    icon: str
    background_color: str
    text_color: str
    role: Optional[CompanyRoleId]  # Responsible role for this stage
    status_mapping: WorkflowStageTypeEnum
    kanban_display: KanbanDisplayEnum
    field_visibility: Dict[str, bool]  # Field name -> visible boolean
    field_validation: Dict[str, Any]  # Field name -> validation rule config (can reference ValidationRule IDs)
    field_candidate_visibility: Dict[str, bool]  # Field name -> visible to candidate boolean

    def __post_init__(self) -> None:
        """Validate the value object"""
        if not self.name or not self.name.strip():
            raise ValueError("Stage name cannot be empty")
        if not self.icon or not self.icon.strip():
            raise ValueError("Stage icon cannot be empty")
        if not self.background_color or not self.background_color.strip():
            raise ValueError("Background color cannot be empty")
        if not self.text_color or not self.text_color.strip():
            raise ValueError("Text color cannot be empty")

    @staticmethod
    def create(
            id: StageId,
            name: str,
            icon: str,
            background_color: str,
            text_color: str,
            status_mapping: WorkflowStageTypeEnum,
            kanban_display: KanbanDisplayEnum = KanbanDisplayEnum.VERTICAL,
            role: Optional[CompanyRoleId] = None,
            field_visibility: Optional[Dict[str, bool]] = None,
            field_validation: Optional[Dict[str, Any]] = None,
            field_candidate_visibility: Optional[Dict[str, bool]] = None,
    ) -> "WorkflowStage":
        """
        Factory method to create a new WorkflowStage
        
        Args:
            id: Stage ID
            name: Stage name
            icon: Icon (emoji or HTML)
            background_color: Background color (hex, rgb, or CSS color name)
            text_color: Text color (hex, rgb, or CSS color name)
            status_mapping: Maps to WorkflowStageTypeEnum
            kanban_display: How to display in Kanban
            role: Responsible role (optional)
            field_visibility: Field visibility configuration
            field_validation: Field validation configuration
            
        Returns:
            WorkflowStage: New instance
        """
        return WorkflowStage(
            id=id,
            name=name.strip(),
            icon=icon.strip(),
            background_color=background_color.strip(),
            text_color=text_color.strip(),
            role=role,
            status_mapping=status_mapping,
            kanban_display=kanban_display,
            field_visibility=field_visibility or {},
            field_validation=field_validation or {},
            field_candidate_visibility=field_candidate_visibility or {},
        )

    def update(
            self,
            name: Optional[str] = None,
            icon: Optional[str] = None,
            background_color: Optional[str] = None,
            text_color: Optional[str] = None,
            role: Optional[CompanyRoleId] = None,
            status_mapping: Optional[WorkflowStageTypeEnum] = None,
            kanban_display: Optional[KanbanDisplayEnum] = None,
            field_visibility: Optional[Dict[str, bool]] = None,
            field_validation: Optional[Dict[str, Any]] = None,
            field_candidate_visibility: Optional[Dict[str, bool]] = None,
    ) -> "WorkflowStage":
        """
        Create a new instance with updated values
        
        Returns:
            WorkflowStage: New instance with updated values
        """
        return WorkflowStage(
            id=self.id,
            name=(name.strip() if name else self.name),
            icon=(icon.strip() if icon else self.icon),
            background_color=(background_color.strip() if background_color else self.background_color),
            text_color=(text_color.strip() if text_color else self.text_color),
            role=role if role is not None else self.role,
            status_mapping=status_mapping if status_mapping is not None else self.status_mapping,
            kanban_display=kanban_display if kanban_display is not None else self.kanban_display,
            field_visibility=field_visibility if field_visibility is not None else self.field_visibility,
            field_validation=field_validation if field_validation is not None else self.field_validation,
            field_candidate_visibility=field_candidate_visibility if field_candidate_visibility is not None else self.field_candidate_visibility,
        )

    def is_field_visible_to_candidate(self, field_name: str,
                                      default_visibility: Optional[Dict[str, bool]] = None) -> bool:
        """
        Check if a field is visible to candidates
        
        Args:
            field_name: Name of the field to check
            default_visibility: Default visibility from custom_fields_config (optional)
            
        Returns:
            bool: True if field is visible to candidates, False otherwise
        """
        # First check stage-specific visibility
        if field_name in self.field_candidate_visibility:
            return self.field_candidate_visibility[field_name]

        # Then check default visibility from workflow config
        if default_visibility and field_name in default_visibility:
            return default_visibility[field_name]

        # Default to False if not specified
        return False
