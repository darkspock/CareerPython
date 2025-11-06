from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.enums.job_position_workflow_status import JobPositionWorkflowStatusEnum
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage


@dataclass
class JobPositionWorkflow:
    """
    Job Position Workflow entity.

    Represents a workflow configuration for managing job positions through stages.
    Each workflow has stages that map to JobPositionStatusEnum values.
    """
    id: JobPositionWorkflowId
    company_id: CompanyId
    name: str
    default_view: ViewTypeEnum
    status: JobPositionWorkflowStatusEnum
    stages: List[WorkflowStage]
    custom_fields_config: Dict[str, Any]  # JSON configuration for custom fields
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: JobPositionWorkflowId,
            company_id: CompanyId,
            name: str,
            default_view: ViewTypeEnum = ViewTypeEnum.KANBAN,
            status: JobPositionWorkflowStatusEnum = JobPositionWorkflowStatusEnum.DRAFT,
            stages: Optional[List[WorkflowStage]] = None,
            custom_fields_config: Optional[Dict[str, Any]] = None,
    ) -> "JobPositionWorkflow":
        """
        Factory method to create a new JobPositionWorkflow

        Args:
            id: Workflow ID
            company_id: Company ID
            name: Workflow name
            default_view: Default view type
            status: Workflow status (default: draft - must be published to use)
            stages: List of stages (optional, can be added later)
            custom_fields_config: Custom fields configuration (optional)
                If None or empty, will be initialized with empty structure

        Returns:
            JobPositionWorkflow: New instance

        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Workflow name cannot be empty")

        # Normalize custom_fields_config
        normalized_config = cls._normalize_custom_fields_config(custom_fields_config or {})

        now = datetime.utcnow()
        return cls(
            id=id,
            company_id=company_id,
            name=name.strip(),
            default_view=default_view,
            status=status,
            stages=stages or [],
            custom_fields_config=normalized_config,
            created_at=now,
            updated_at=now,
        )

    def update(
            self,
            name: str,
            default_view: Optional[ViewTypeEnum] = None,
            status: Optional[JobPositionWorkflowStatusEnum] = None,
            custom_fields_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update workflow information

        Args:
            name: New workflow name
            default_view: New default view (optional)
            status: New workflow status (optional)
            custom_fields_config: New custom fields config (optional)

        Raises:
            ValueError: If name is empty

        Note:
            custom_fields_config should follow this structure:
            {
                "fields": {
                    "field_name": {
                        "type": "text|number|date|select|object",
                        "label": "Field Label",
                        "required": False,
                        "candidate_visible": True,
                        "default_visibility": True
                    }
                },
                "field_candidate_visibility_default": {
                    "field_name": True
                },
                "field_types": {
                    "field_name": "text"
                },
                "field_labels": {
                    "field_name": "Field Label"
                },
                "field_required": {
                    "field_name": False
                },
                "field_validation": {
                    "field_name": {...}
                }
            }
        """
        if not name or not name.strip():
            raise ValueError("Workflow name cannot be empty")

        self.name = name.strip()
        if default_view is not None:
            self.default_view = default_view
        if status is not None:
            self.status = status
        if custom_fields_config is not None:
            # Normalize custom_fields_config before setting
            self.custom_fields_config = self._normalize_custom_fields_config(custom_fields_config)
        self.updated_at = datetime.utcnow()

    def get_field_candidate_visibility_default(self) -> Dict[str, bool]:
        """
        Get default candidate visibility for all fields.

        Returns:
            Dict[str, bool]: Field name -> visibility boolean
        """
        if "field_candidate_visibility_default" in self.custom_fields_config:
            value = self.custom_fields_config["field_candidate_visibility_default"]
            if isinstance(value, dict):
                return {k: bool(v) for k, v in value.items()}

        # Fallback: extract from fields config if available
        visibility_default: Dict[str, bool] = {}
        if "fields" in self.custom_fields_config:
            for field_name, field_config in self.custom_fields_config["fields"].items():
                if isinstance(field_config, dict):
                    visibility_default[field_name] = bool(field_config.get("candidate_visible", False))

        return visibility_default

    def get_field_config(self, field_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific field.

        Args:
            field_name: Name of the field

        Returns:
            Dict with field configuration or None if not found
        """
        if "fields" in self.custom_fields_config and field_name in self.custom_fields_config["fields"]:
            value = self.custom_fields_config["fields"][field_name]
            if isinstance(value, dict):
                return value
        return None

    @staticmethod
    def _normalize_custom_fields_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize custom_fields_config to ensure it has the expected structure.

        This method ensures that:
        - "fields" dict exists and contains field definitions
        - "field_candidate_visibility_default" dict exists
        - Field definitions include "candidate_visible" property
        - Default visibility is extracted from field definitions if not explicitly set

        Args:
            config: Raw custom_fields_config dictionary

        Returns:
            Dict[str, Any]: Normalized configuration
        """
        normalized = config.copy() if config else {}

        # Ensure "fields" dict exists
        if "fields" not in normalized:
            normalized["fields"] = {}

        # Extract default visibility from field definitions if not explicitly set
        if "field_candidate_visibility_default" not in normalized:
            normalized["field_candidate_visibility_default"] = {}

            # Extract from fields config
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict):
                    # Check for "candidate_visible" or "default_visibility" in field config
                    candidate_visible = field_config.get("candidate_visible", False)
                    default_visibility = field_config.get("default_visibility", candidate_visible)
                    normalized["field_candidate_visibility_default"][field_name] = default_visibility

        # Ensure backward compatibility: if "field_candidate_visibility_default" exists but is empty,
        # try to populate it from fields
        if not normalized["field_candidate_visibility_default"] and normalized["fields"]:
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict):
                    candidate_visible = field_config.get("candidate_visible", False)
                    default_visibility = field_config.get("default_visibility", candidate_visible)
                    normalized["field_candidate_visibility_default"][field_name] = default_visibility

        # Ensure other optional fields exist for backward compatibility
        if "field_types" not in normalized:
            normalized["field_types"] = {}
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict):
                    normalized["field_types"][field_name] = field_config.get("type", "text")

        if "field_labels" not in normalized:
            normalized["field_labels"] = {}
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict):
                    normalized["field_labels"][field_name] = field_config.get("label", field_name)

        if "field_required" not in normalized:
            normalized["field_required"] = {}
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict):
                    normalized["field_required"][field_name] = field_config.get("required", False)

        if "field_validation" not in normalized:
            normalized["field_validation"] = {}
            for field_name, field_config in normalized["fields"].items():
                if isinstance(field_config, dict) and "validation" in field_config:
                    normalized["field_validation"][field_name] = field_config["validation"]

        return normalized

    def add_field_config(
            self,
            field_name: str,
            field_type: str = "text",
            label: Optional[str] = None,
            required: bool = False,
            candidate_visible: bool = False,
            validation: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add or update a field configuration.

        Args:
            field_name: Name of the field
            field_type: Type of field (text, number, date, select, object)
            label: Display label for the field
            required: Whether the field is required
            candidate_visible: Whether the field is visible to candidates by default
            validation: Validation rules for the field
        """
        if "fields" not in self.custom_fields_config:
            self.custom_fields_config["fields"] = {}

        self.custom_fields_config["fields"][field_name] = {
            "type": field_type,
            "label": label or field_name,
            "required": required,
            "candidate_visible": candidate_visible,
            "default_visibility": candidate_visible,
        }

        if validation:
            self.custom_fields_config["fields"][field_name]["validation"] = validation

        # Update default visibility
        if "field_candidate_visibility_default" not in self.custom_fields_config:
            self.custom_fields_config["field_candidate_visibility_default"] = {}

        self.custom_fields_config["field_candidate_visibility_default"][field_name] = candidate_visible

        # Update backward compatibility fields
        if "field_types" not in self.custom_fields_config:
            self.custom_fields_config["field_types"] = {}
        self.custom_fields_config["field_types"][field_name] = field_type

        if "field_labels" not in self.custom_fields_config:
            self.custom_fields_config["field_labels"] = {}
        self.custom_fields_config["field_labels"][field_name] = label or field_name

        if "field_required" not in self.custom_fields_config:
            self.custom_fields_config["field_required"] = {}
        self.custom_fields_config["field_required"][field_name] = required

        if validation:
            if "field_validation" not in self.custom_fields_config:
                self.custom_fields_config["field_validation"] = {}
            self.custom_fields_config["field_validation"][field_name] = validation

        self.updated_at = datetime.utcnow()

    def remove_field_config(self, field_name: str) -> None:
        """
        Remove a field configuration.

        Args:
            field_name: Name of the field to remove
        """
        if "fields" in self.custom_fields_config:
            self.custom_fields_config["fields"].pop(field_name, None)

        if "field_candidate_visibility_default" in self.custom_fields_config:
            self.custom_fields_config["field_candidate_visibility_default"].pop(field_name, None)

        # Remove from backward compatibility fields
        for key in ["field_types", "field_labels", "field_required", "field_validation"]:
            if key in self.custom_fields_config:
                self.custom_fields_config[key].pop(field_name, None)

        self.updated_at = datetime.utcnow()

    def add_stage(self, stage: WorkflowStage) -> None:
        """
        Add a stage to the workflow

        Args:
            stage: Stage to add

        Raises:
            ValueError: If stage with same ID already exists
        """
        if any(s.id.value == stage.id.value for s in self.stages):
            raise ValueError(f"Stage with ID {stage.id.value} already exists in workflow")

        self.stages.append(stage)
        self.updated_at = datetime.utcnow()

    def remove_stage(self, stage_id: str) -> None:
        """
        Remove a stage from the workflow

        Args:
            stage_id: ID of stage to remove

        Raises:
            ValueError: If stage not found
        """
        initial_count = len(self.stages)
        self.stages = [s for s in self.stages if s.id.value != stage_id]

        if len(self.stages) == initial_count:
            raise ValueError(f"Stage with ID {stage_id} not found in workflow")

        self.updated_at = datetime.utcnow()

    def update_stage(self, stage_id: str, updated_stage: WorkflowStage) -> None:
        """
        Update a stage in the workflow

        Args:
            stage_id: ID of stage to update
            updated_stage: Updated stage (must have same ID)

        Raises:
            ValueError: If stage not found or IDs don't match
        """
        if stage_id != updated_stage.id.value:
            raise ValueError("Stage ID mismatch")

        for i, stage in enumerate(self.stages):
            if stage.id.value == stage_id:
                self.stages[i] = updated_stage
                self.updated_at = datetime.utcnow()
                return

        raise ValueError(f"Stage with ID {stage_id} not found in workflow")

    def get_stage_by_id(self, stage_id: str) -> Optional[WorkflowStage]:
        """
        Get a stage by ID

        Args:
            stage_id: Stage ID to find

        Returns:
            WorkflowStage if found, None otherwise
        """
        for stage in self.stages:
            if stage.id.value == stage_id:
                return stage
        return None
