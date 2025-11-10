"""Enum metadata controller for frontend consumption"""
from enum import Enum
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from src.candidate_bc.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company_bc.job_position.domain.enums import WorkLocationTypeEnum, ContractTypeEnum
from src.company_bc.job_position.domain.enums import EmploymentType
from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.framework.domain.enums.job_category import JobCategoryEnum


class EnumOption(BaseModel):
    """Single enum option"""
    value: str
    label: str


class EnumMetadataResponse(BaseModel):
    """Response containing all enum definitions"""
    languages: List[EnumOption]
    language_levels: List[EnumOption]
    desired_roles: List[EnumOption]
    work_location_types: List[EnumOption]
    employment_types: List[EnumOption]
    contract_types: List[EnumOption]
    experience_levels: List[EnumOption]
    job_categories: List[EnumOption]


class EnumController:
    """Controller for enum metadata operations"""

    def get_enum_metadata(self) -> EnumMetadataResponse:
        """Get all enum definitions for frontend consumption"""

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

        # Custom labels for better UX
        language_labels = {
            'english': 'English',
            'spanish': 'Spanish',
            'portuguese': 'Portuguese',
            'italian': 'Italian',
            'french': 'French',
            'chinese': 'Chinese',
            'german': 'German',
            'japanese': 'Japanese',
            'russian': 'Russian',
            'arabic': 'Arabic'
        }

        language_level_labels = {
            'none': 'None',
            'basic': 'Basic',
            'conversational': 'Conversational',
            'professional': 'Professional'
        }

        role_labels = {
            'manage_people': 'Manage People',
            'lead_initiatives': 'Lead Initiatives',
            'technology': 'Technology',
            'sales': 'Sales',
            'financial': 'Financial',
            'hr': 'HR',
            'executive': 'Executive',
            'operations': 'Operations',
            'marketing': 'Marketing',
            'product': 'Product',
            'legal_compliance': 'Legal & Compliance',
            'customer_success': 'Customer Success'
        }

        work_location_labels = {
            'on_site': 'On-site',
            'remote': 'Remote',
            'hybrid': 'Hybrid',
            'flexible': 'Flexible'
        }

        employment_type_labels = {
            'full_time': 'Full Time',
            'part_time': 'Part Time',
            'contract': 'Contract',
            'temporary': 'Temporary',
            'internship': 'Internship',
            'volunteer': 'Volunteer',
            'other': 'Other'
        }

        contract_type_labels = {
            'full_time': 'Full Time',
            'part_time': 'Part Time',
            'contract': 'Contract',
            'internship': 'Internship'
        }

        experience_level_labels = {
            'junior': 'Junior',
            'mid': 'Mid Level',
            'senior': 'Senior',
            'lead': 'Lead'
        }

        job_category_labels = {
            'technology': 'Technology',
            'marketing': 'Marketing',
            'sales': 'Sales',
            'design': 'Design',
            'operations': 'Operations',
            'finance': 'Finance',
            'hr': 'Human Resources',
            'customer_service': 'Customer Service',
            'other': 'Other'
        }

        return EnumMetadataResponse(
            languages=enum_to_options(LanguageEnum, language_labels),
            language_levels=enum_to_options(LanguageLevelEnum, language_level_labels),
            desired_roles=enum_to_options(PositionRoleEnum, role_labels),
            work_location_types=enum_to_options(WorkLocationTypeEnum, work_location_labels),
            employment_types=enum_to_options(EmploymentType, employment_type_labels),
            contract_types=enum_to_options(ContractTypeEnum, contract_type_labels),
            experience_levels=enum_to_options(JobPositionLevelEnum, experience_level_labels),
            job_categories=enum_to_options(JobCategoryEnum, job_category_labels)
        )
