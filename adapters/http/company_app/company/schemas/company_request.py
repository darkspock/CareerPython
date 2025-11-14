from typing import Optional, Dict, Any

from pydantic import BaseModel, field_validator

from src.company_bc.company.domain.enums import CompanyTypeEnum


class CreateCompanyRequest(BaseModel):
    """Request schema to create a company"""
    name: str
    domain: str
    logo_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    company_type: Optional[CompanyTypeEnum] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not empty and has minimum length"""
        if not v or not v.strip():
            raise ValueError('Company name cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('Company name must be at least 3 characters')
        if len(v.strip()) > 255:
            raise ValueError('Company name cannot exceed 255 characters')
        return v.strip()

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        """Validate domain is not empty"""
        if not v or not v.strip():
            raise ValueError('Company domain cannot be empty')
        if len(v.strip()) > 255:
            raise ValueError('Company domain cannot exceed 255 characters')
        return v.strip().lower()


class UpdateCompanyRequest(BaseModel):
    """Request schema to update a company"""
    name: str
    domain: str
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Dict[str, Any]
    company_type: Optional[CompanyTypeEnum] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is not empty and has minimum length"""
        if not v or not v.strip():
            raise ValueError('Company name cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('Company name must be at least 3 characters')
        if len(v.strip()) > 255:
            raise ValueError('Company name cannot exceed 255 characters')
        return v.strip()

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        """Validate domain is not empty"""
        if not v or not v.strip():
            raise ValueError('Company domain cannot be empty')
        if len(v.strip()) > 255:
            raise ValueError('Company domain cannot exceed 255 characters')
        return v.strip().lower()

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        """Validate slug format"""
        if v is None:
            return None
        if not v.strip():
            return None
        slug = v.strip().lower()
        # Only allow alphanumeric and hyphens
        if not slug.replace('-', '').isalnum():
            raise ValueError('Slug can only contain letters, numbers, and hyphens')
        if len(slug) > 255:
            raise ValueError('Slug cannot exceed 255 characters')
        return slug


class SuspendCompanyRequest(BaseModel):
    """Request schema to suspend a company"""
    reason: Optional[str] = None

    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v: Optional[str]) -> Optional[str]:
        """Validate reason if provided"""
        if v and len(v.strip()) > 500:
            raise ValueError('Suspension reason cannot exceed 500 characters')
        return v.strip() if v else None
