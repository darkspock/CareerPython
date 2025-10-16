#!/usr/bin/env python3
"""
Generate OpenAPI schema for enums that can be consumed by TypeScript generators
"""

import json
from typing import Dict, Any

from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.job_position.domain.enums import WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.domain.enums.employment_type import EmploymentType


def enum_to_openapi_schema(enum_class, description: str = None) -> Dict[str, Any]:
    """Convert Python enum to OpenAPI schema"""
    return {
        "type": "string",
        "enum": [item.value for item in enum_class],
        "description": description or f"Available {enum_class.__name__} values"
    }


def generate_openapi_enums():
    """Generate OpenAPI schema for all enums"""

    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Enum Definitions",
            "version": "1.0.0"
        },
        "components": {
            "schemas": {
                "LanguageEnum": enum_to_openapi_schema(
                    LanguageEnum,
                    "Supported languages for job positions"
                ),
                "LanguageLevelEnum": enum_to_openapi_schema(
                    LanguageLevelEnum,
                    "Language proficiency levels"
                ),
                "PositionRoleEnum": enum_to_openapi_schema(
                    PositionRoleEnum,
                    "Desired roles for candidates"
                ),
                "WorkLocationTypeEnum": enum_to_openapi_schema(
                    WorkLocationTypeEnum,
                    "Work location arrangements"
                ),
                "EmploymentTypeEnum": enum_to_openapi_schema(
                    EmploymentType,
                    "Employment types"
                ),
                "ContractTypeEnum": enum_to_openapi_schema(
                    ContractTypeEnum,
                    "Contract types"
                )
            }
        }
    }

    # Write to file
    with open("client-vite/src/types/enum-schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    print("✅ Generated OpenAPI enum schema")
    print("💡 Use with: npx openapi-typescript enum-schema.json --output src/types/generated-enums.ts")


if __name__ == "__main__":
    generate_openapi_enums()