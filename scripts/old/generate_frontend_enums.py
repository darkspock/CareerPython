#!/usr/bin/env python3
"""
Script to generate TypeScript enum definitions from Python enums.
Run this during build process to keep frontend enums in sync.
"""

import os

# Import all the enums we want to generate
from src.candidate_bc.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company_bc.job_position.domain.enums import WorkLocationTypeEnum, ContractTypeEnum
from src.company_bc.job_position.domain.enums import EmploymentType
from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.framework.domain.enums.job_category import JobCategoryEnum


def format_label(enum_name: str, enum_value: str) -> str:
    """Convert enum value to human-readable label"""
    # Custom label mappings
    custom_labels = {
        'LanguageEnum': {
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
        },
        'LanguageLevelEnum': {
            'none': 'None',
            'basic': 'Basic',
            'conversational': 'Conversational',
            'professional': 'Professional'
        },
        'PositionRoleEnum': {
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
        },
        'WorkLocationTypeEnum': {
            'on_site': 'On-site',
            'remote': 'Remote',
            'hybrid': 'Hybrid',
            'flexible': 'Flexible'
        }
    }

    if enum_name in custom_labels and enum_value in custom_labels[enum_name]:
        return custom_labels[enum_name][enum_value]

    # Default: convert snake_case to Title Case
    return enum_value.replace('_', ' ').title()


def generate_ts_enum_options(enum_class: type, enum_name: str) -> str:
    """Generate TypeScript enum options array"""
    options = []

    for enum_item in enum_class:
        value = enum_item.value
        label = format_label(enum_name, value)
        options.append(f"  {{ value: '{value}', label: '{label}' }}")

    return f"export const {enum_name.upper()}_OPTIONS = [\n" + ",\n".join(options) + "\n] as const;"


def generate_typescript_enums():
    """Generate TypeScript file with all enum options"""

    enums_to_generate = [
        (LanguageEnum, 'Language'),
        (LanguageLevelEnum, 'LanguageLevel'),
        (PositionRoleEnum, 'PositionRole'),
        (WorkLocationTypeEnum, 'WorkLocationType'),
        (EmploymentType, 'EmploymentType'),
        (ContractTypeEnum, 'ContractType'),
        (JobPositionLevelEnum, 'JobPositionLevel'),
        (JobCategoryEnum, 'JobCategory')
    ]

    output_lines = [
        "// AUTO-GENERATED FILE - Do not edit manually",
        "// Generated from Python enums using scripts/generate_frontend_enums.py",
        "",
        "export interface EnumOption {",
        "  value: string;",
        "  label: string;",
        "}",
        ""
    ]

    for enum_class, enum_name in enums_to_generate:
        ts_enum = generate_ts_enum_options(enum_class, enum_name)
        output_lines.append(ts_enum)
        output_lines.append("")

    # Write to frontend types file
    output_path = "client-vite/src/types/generated-enums.ts"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines))

    print(f"✅ Generated TypeScript enums at: {output_path}")
    print(f"📊 Generated {len(enums_to_generate)} enum definitions")


if __name__ == "__main__":
    generate_typescript_enums()