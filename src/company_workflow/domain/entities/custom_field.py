from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.field_option import FieldOption
from src.company_workflow.domain.enums.field_type import FieldType


@dataclass(frozen=True)
class CustomField:
    """Custom field entity - represents a configurable field in a workflow"""
    id: CustomFieldId
    workflow_id: CompanyWorkflowId
    field_key: str  # Unique identifier for the field (e.g., "expected_salary")
    field_name: str  # Display name (e.g., "Expected Salary")
    field_type: FieldType
    field_config: Optional[Dict[str, Any]]  # Field-specific configuration (options, validation, etc.)
    order_index: int  # Position in the workflow field list
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: CustomFieldId,
        workflow_id: CompanyWorkflowId,
        field_key: str,
        field_name: str,
        field_type: FieldType,
        order_index: int,
        field_config: Optional[Dict[str, Any]] = None
    ) -> "CustomField":
        """Factory method to create a new custom field"""
        if not field_key:
            raise ValueError("Field key cannot be empty")
        if not field_key.isidentifier():
            raise ValueError("Field key must be a valid identifier (alphanumeric and underscores only)")
        if not field_name:
            raise ValueError("Field name cannot be empty")
        if len(field_name) > 255:
            raise ValueError("Field name cannot exceed 255 characters")
        if order_index < 0:
            raise ValueError("Order index must be non-negative")

        # Validate field config based on field type
        validated_config = CustomField._validate_field_config(field_type, field_config)

        now = datetime.utcnow()
        return CustomField(
            id=id,
            workflow_id=workflow_id,
            field_key=field_key,
            field_name=field_name,
            field_type=field_type,
            field_config=validated_config,
            order_index=order_index,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        field_name: str,
        field_type: FieldType,
        field_config: Optional[Dict[str, Any]] = None
    ) -> "CustomField":
        """Update field information"""
        if not field_name:
            raise ValueError("Field name cannot be empty")
        if len(field_name) > 255:
            raise ValueError("Field name cannot exceed 255 characters")

        # Validate field config based on field type
        validated_config = CustomField._validate_field_config(field_type, field_config)

        return CustomField(
            id=self.id,
            workflow_id=self.workflow_id,
            field_key=self.field_key,
            field_name=field_name,
            field_type=field_type,
            field_config=validated_config,
            order_index=self.order_index,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def reorder(self, new_order_index: int) -> "CustomField":
        """Change the order of this field"""
        if new_order_index < 0:
            raise ValueError("Order index must be non-negative")

        return CustomField(
            id=self.id,
            workflow_id=self.workflow_id,
            field_key=self.field_key,
            field_name=self.field_name,
            field_type=self.field_type,
            field_config=self.field_config,
            order_index=new_order_index,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    @staticmethod
    def _validate_field_config(
        field_type: FieldType,
        field_config: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Validate field configuration based on field type"""
        if field_config is None:
            return None

        # Validate based on field type
        if field_type in [FieldType.DROPDOWN, FieldType.MULTI_SELECT, FieldType.RADIO, FieldType.CHECKBOX]:
            if "options" not in field_config:
                raise ValueError(f"{field_type.value} field must have 'options' in config")
            if not isinstance(field_config["options"], list):
                raise ValueError(f"{field_type.value} options must be a list")
            if len(field_config["options"]) == 0:
                raise ValueError(f"{field_type.value} must have at least one option")
            
            # Validate options - support both old format (strings) and new format (objects with id, sort, labels)
            for i, option in enumerate(field_config["options"]):
                if isinstance(option, dict):
                    # New format: if it's a dict, it should have the proper structure
                    # But we don't enforce it strictly to allow mixed formats during transition
                    if "id" in option and "labels" in option:
                        # It's in new format - validate it
                        if "sort" not in option:
                            raise ValueError(f"Option at index {i} in new format must have 'sort' field")
                        if not isinstance(option["labels"], list) or len(option["labels"]) == 0:
                            raise ValueError(f"Option at index {i} must have at least one label in 'labels' array")
                        for label in option["labels"]:
                            if not isinstance(label, dict) or "language" not in label or "label" not in label:
                                raise ValueError(f"Label in option at index {i} must have 'language' and 'label' fields")
                    # If dict doesn't have id/labels, it might be a different config structure - allow it
                elif not isinstance(option, str):
                    # Old format should be strings
                    raise ValueError(f"Option at index {i} must be either a string (old format) or an object with id/sort/labels (new format)")

        if field_type == FieldType.NUMBER:
            if "min" in field_config and "max" in field_config:
                if field_config["min"] > field_config["max"]:
                    raise ValueError("Number field min value cannot be greater than max value")

        if field_type == FieldType.CURRENCY:
            if "currency_code" in field_config:
                if not isinstance(field_config["currency_code"], str):
                    raise ValueError("Currency code must be a string")
                if len(field_config["currency_code"]) != 3:
                    raise ValueError("Currency code must be 3 characters (ISO 4217)")

        if field_type == FieldType.FILE:
            if "allowed_extensions" in field_config:
                if not isinstance(field_config["allowed_extensions"], list):
                    raise ValueError("Allowed extensions must be a list")
                for ext in field_config["allowed_extensions"]:
                    if not isinstance(ext, str):
                        raise ValueError("File extensions must be strings")
                    if not ext.startswith("."):
                        raise ValueError("File extensions must start with a dot (.)")

        if field_type == FieldType.TEXT:
            if "max_length" in field_config:
                if not isinstance(field_config["max_length"], int):
                    raise ValueError("Max length must be an integer")
                if field_config["max_length"] < 1:
                    raise ValueError("Max length must be at least 1")

        return field_config

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a value from field configuration"""
        if self.field_config is None:
            return default
        return self.field_config.get(key, default)

    def has_options(self) -> bool:
        """Check if this field type supports options"""
        return self.field_type in [
            FieldType.DROPDOWN,
            FieldType.MULTI_SELECT,
            FieldType.RADIO,
            FieldType.CHECKBOX
        ]

    def get_options(self, language: Optional[str] = None) -> List[str]:
        """
        Get options as simple strings (for backward compatibility)
        Uses new format if available, falls back to old format
        
        Args:
            language: Language code for i18n labels (defaults to first label)
        
        Returns:
            List of option label strings
        """
        if not self.has_options():
            return []
        options = self.get_config_value("options", [])
        if not options:
            return []
        
        result = []
        for option in options:
            if isinstance(option, dict):
                # New format: extract label
                try:
                    field_option = FieldOption.from_dict(option)
                    result.append(field_option.get_label(language))
                except Exception:
                    # Fallback if structure is invalid
                    if "labels" in option and option["labels"]:
                        result.append(option["labels"][0].get("label", ""))
                    elif "label" in option:
                        result.append(option["label"])
            elif isinstance(option, str):
                # Old format: direct string
                result.append(option)
        
        return result

    def get_options_as_objects(self) -> List[FieldOption]:
        """
        Get options as FieldOption objects (new format)
        Converts old format to new format automatically
        
        Returns:
            List of FieldOption objects
        """
        if not self.has_options():
            return []
        options = self.get_config_value("options", [])
        if not options:
            return []
        
        result = []
        for i, option in enumerate(options):
            if isinstance(option, dict):
                # New format: convert from dict
                try:
                    result.append(FieldOption.from_dict(option))
                except Exception as e:
                    # If conversion fails, create from legacy format
                    if "label" in option:
                        legacy_label = option["label"]
                    elif "labels" in option and option["labels"]:
                        legacy_label = option["labels"][0].get("label", "")
                    else:
                        legacy_label = str(option)
                    result.append(FieldOption.create(
                        labels=[{"language": "en", "label": legacy_label}],
                        sort=option.get("sort", i)
                    ))
            elif isinstance(option, str):
                # Old format: convert to new format
                result.append(FieldOption.create(
                    labels=[{"language": "en", "label": option}],
                    sort=i
                ))
        
        return result

    def update_options(self, new_options: List[FieldOption]) -> "CustomField":
        """
        Update options with new FieldOption objects
        
        Args:
            new_options: List of FieldOption objects
        
        Returns:
            New CustomField instance with updated options
        """
        if not self.has_options():
            raise ValueError(f"{self.field_type.value} fields do not support options")
        
        if not new_options:
            raise ValueError("Must have at least one option")
        
        # Convert to dict format
        options_dict = [option.to_dict() for option in new_options]
        
        # Sort by sort index
        options_dict.sort(key=lambda x: x["sort"])
        
        # Update field_config
        new_config = self.field_config.copy() if self.field_config else {}
        new_config["options"] = options_dict
        
        return self.update(
            field_name=self.field_name,
            field_type=self.field_type,
            field_config=new_config
        )
