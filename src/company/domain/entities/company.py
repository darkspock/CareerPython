from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from src.company.domain.enums import CompanyStatusEnum
from src.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company.domain.value_objects.company_id import CompanyId
from src.user.domain.value_objects.UserId import UserId


@dataclass
class Company:
    id: CompanyId
    name: str
    user_id: Optional[UserId]
    created_at: datetime
    updated_at: datetime
    sector: Optional[str] = None
    size: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None
    culture: Optional[Dict[str, Any]] = field(default_factory=dict)
    external_data: Optional[Dict[str, Any]] = field(default_factory=dict)
    status: CompanyStatusEnum = CompanyStatusEnum.PENDING

    @staticmethod
    def create(
            id: CompanyId,
            user_id: Optional[UserId],
            name: str,
            sector: Optional[str] = None,
            size: Optional[int] = None,
            location: Optional[str] = None,
            website: Optional[str] = None,
            culture: Optional[Dict[str, Any]] = None,
            external_data: Optional[Dict[str, Any]] = None
    ) -> 'Company':
        """Factory method to create a new company"""
        now = datetime.utcnow()
        return Company(
            id=id,
            user_id=user_id,
            name=name,
            sector=sector,
            size=size,
            location=location,
            website=website,
            culture=culture or {},
            external_data=external_data or {},
            status=CompanyStatusEnum.PENDING,
            created_at=now,
            updated_at=now
        )

    def __post_init__(self) -> None:
        """Validate company data after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate company data"""
        if not self.name or len(self.name.strip()) == 0:
            raise CompanyValidationError("Company name is required")

        # user_id is now optional - no validation needed

        if self.size is not None and self.size < 1:
            raise CompanyValidationError("Company size must be positive")

        # No website validation as requested by user

    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation"""
        return url.startswith(('http://', 'https://')) and '.' in url

    def approve(self) -> None:
        """Approve the company (set to active)"""
        if self.status == CompanyStatusEnum.ACTIVE:
            return
        self.status = CompanyStatusEnum.ACTIVE
        self.updated_at = datetime.utcnow()

    def reject(self) -> None:
        """Reject the company"""
        if self.status == CompanyStatusEnum.REJECTED:
            return
        self.status = CompanyStatusEnum.REJECTED
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the company"""
        if self.status == CompanyStatusEnum.ACTIVE:
            return
        self.status = CompanyStatusEnum.ACTIVE
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the company"""
        if self.status == CompanyStatusEnum.INACTIVE:
            return
        self.status = CompanyStatusEnum.INACTIVE
        self.updated_at = datetime.utcnow()

    def update_details(
            self,
            name: Optional[str] = None,
            sector: Optional[str] = None,
            size: Optional[int] = None,
            location: Optional[str] = None,
            website: Optional[str] = None,
            culture: Optional[Dict[str, Any]] = None,
            external_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update company details"""
        if name is not None:
            self.name = name
        if sector is not None:
            self.sector = sector
        if size is not None:
            self.size = size
        if location is not None:
            self.location = location
        if website is not None:
            self.website = website
        if culture is not None:
            self.culture = culture
        if external_data is not None:
            self.external_data = external_data

        self.updated_at = datetime.utcnow()
        self._validate()

    def is_approved(self) -> bool:
        """Check if company is approved"""
        return self.status == CompanyStatusEnum.ACTIVE

    def is_active(self) -> bool:
        """Check if company is active"""
        return self.status == CompanyStatusEnum.ACTIVE

    def can_create_job_positions(self) -> bool:
        """Check if company can create job positions"""
        return self.status in [CompanyStatusEnum.ACTIVE, CompanyStatusEnum.ACTIVE]
