"""Enum metadata controller for company frontend consumption"""
from enum import Enum
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from src.company_workflow.domain.enums.stage_type import StageType


class EnumOption(BaseModel):
    """Single enum option"""
    value: str
    label: str


class CompanyEnumMetadataResponse(BaseModel):
    """Response containing all enum definitions for company"""
    stage_types: List[EnumOption]


class CompanyEnumController:
    """Controller for company enum metadata operations"""

    def get_enum_metadata(self) -> CompanyEnumMetadataResponse:
        """Get all enum definitions for company frontend consumption"""

        # Helper function to convert enum to options with proper labels
        def enum_to_options(enum_class: Type[Enum], custom_labels: Optional[Dict[str, str]] = None) -> List[EnumOption]:
            options = []
            for enum_item in enum_class:
                value = enum_item.value
                # Use custom label if provided, otherwise format the enum name
                if custom_labels and value in custom_labels:
                    label = custom_labels[value]
                else:
                    # Convert enum name to human-readable label
                    label = enum_item.name.replace('_', ' ').title()

                options.append(EnumOption(value=value, label=label))
            return options

        # Custom labels for stage types
        stage_type_labels = {
            'initial': 'Initial',
            'intermediate': 'Intermediate',
            'final': 'Final',
            'custom': 'Custom'
        }

        return CompanyEnumMetadataResponse(
            stage_types=enum_to_options(StageType, stage_type_labels)
        )
