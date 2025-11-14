"""Request schemas for company registration"""
from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr

from src.company_bc.company.domain.enums import CompanyTypeEnum


class CompanyRegistrationRequest(BaseModel):
    """Request schema to register a company with a new user"""

    # User data
    email: EmailStr
    password: str
    full_name: str

    # Company data
    company_name: str
    domain: str
    logo_url: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    company_type: Optional[CompanyTypeEnum] = None  # Company type for onboarding customization

    # Options
    initialize_workflows: bool = True  # Whether to initialize default workflows
    include_example_data: bool = False  # Whether to include sample data
    accept_terms: bool
    accept_privacy: bool

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: EmailStr) -> EmailStr:
        """Validate email format"""
        if not v or not v.strip():
            raise ValueError('Email is required')
        return v.strip().lower()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if not v:
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name"""
        if not v or not v.strip():
            raise ValueError('Full name is required')
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        return v.strip()

    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        """Validate company name"""
        if not v or not v.strip():
            raise ValueError('Company name is required')
        if len(v.strip()) < 3:
            raise ValueError('Company name must be at least 3 characters')
        return v.strip()

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        """Validate domain format"""
        if not v or not v.strip():
            raise ValueError('Domain is required')
        domain = v.strip().lower()
        # Basic domain validation (allow letters, numbers, dots, hyphens)
        if not all(c.isalnum() or c in '.-' for c in domain):
            raise ValueError('Domain contains invalid characters')
        if len(domain) > 255:
            raise ValueError('Domain cannot exceed 255 characters')
        return domain

    @field_validator('accept_terms', 'accept_privacy')
    @classmethod
    def validate_terms_accepted(cls, v: bool) -> bool:
        """Validate that terms and privacy are accepted"""
        if not v:
            raise ValueError('You must accept the terms and conditions and privacy policy')
        return v


class LinkUserRequest(BaseModel):
    """Request schema to link an existing user to a new company"""

    # User authentication
    email: EmailStr
    password: str

    # Company data
    company_name: str
    domain: str
    logo_url: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    company_type: Optional[CompanyTypeEnum] = None  # Company type for onboarding customization

    # Options
    initialize_workflows: bool = True  # Whether to initialize default workflows
    include_example_data: bool = False  # Whether to include sample data
    accept_terms: bool
    accept_privacy: bool

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: EmailStr) -> EmailStr:
        """Validate email format"""
        if not v or not v.strip():
            raise ValueError('Email is required')
        return v.strip().lower()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password"""
        if not v:
            raise ValueError('Password is required')
        return v

    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        """Validate company name"""
        if not v or not v.strip():
            raise ValueError('Company name is required')
        if len(v.strip()) < 3:
            raise ValueError('Company name must be at least 3 characters')
        return v.strip()

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        """Validate domain format"""
        if not v or not v.strip():
            raise ValueError('Domain is required')
        domain = v.strip().lower()
        if not all(c.isalnum() or c in '.-' for c in domain):
            raise ValueError('Domain contains invalid characters')
        if len(domain) > 255:
            raise ValueError('Domain cannot exceed 255 characters')
        return domain

    @field_validator('accept_terms', 'accept_privacy')
    @classmethod
    def validate_terms_accepted(cls, v: bool) -> bool:
        """Validate that terms and privacy are accepted"""
        if not v:
            raise ValueError('You must accept the terms and conditions and privacy policy')
        return v
