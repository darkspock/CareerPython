import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.auth_bc.user_registration.domain.enums import RegistrationStatusEnum, ProcessingStatusEnum
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId


@dataclass
class UserRegistration:
    """Domain entity for user registration before email verification"""

    id: UserRegistrationId
    email: str
    verification_token: str
    token_expires_at: datetime
    status: RegistrationStatusEnum
    processing_status: ProcessingStatusEnum
    created_at: datetime
    updated_at: datetime

    # Optional fields
    company_id: Optional[str] = None
    job_position_id: Optional[str] = None
    existing_user_id: Optional[str] = None

    # PDF file data
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None

    # Extracted content
    text_content: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None

    def verify(self) -> None:
        """Mark registration as verified"""
        if self.status == RegistrationStatusEnum.EXPIRED:
            raise ValueError("Cannot verify expired registration")
        if self.status == RegistrationStatusEnum.VERIFIED:
            raise ValueError("Registration already verified")

        self.status = RegistrationStatusEnum.VERIFIED
        self.updated_at = datetime.utcnow()

    def expire(self) -> None:
        """Mark registration as expired"""
        if self.status == RegistrationStatusEnum.VERIFIED:
            raise ValueError("Cannot expire verified registration")

        self.status = RegistrationStatusEnum.EXPIRED
        self.updated_at = datetime.utcnow()

    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.utcnow() > self.token_expires_at

    def is_verified(self) -> bool:
        """Check if registration is verified"""
        return self.status == RegistrationStatusEnum.VERIFIED

    def set_processing_status(self, status: ProcessingStatusEnum, error: Optional[str] = None) -> None:
        """Update PDF processing status"""
        self.processing_status = status
        self.updated_at = datetime.utcnow()

    def set_extracted_content(self, text_content: str, extracted_data: Dict[str, Any]) -> None:
        """Set extracted PDF content"""
        self.text_content = text_content
        self.extracted_data = extracted_data
        self.processing_status = ProcessingStatusEnum.COMPLETED
        self.updated_at = datetime.utcnow()

    def link_to_existing_user(self, user_id: str) -> None:
        """Link registration to an existing user"""
        self.existing_user_id = user_id
        self.updated_at = datetime.utcnow()

    def has_pdf(self) -> bool:
        """Check if registration has a PDF attached"""
        return self.file_name is not None and self.file_size is not None

    def is_processing_complete(self) -> bool:
        """Check if PDF processing is complete"""
        return self.processing_status == ProcessingStatusEnum.COMPLETED

    @staticmethod
    def create(
            id: UserRegistrationId,
            email: str,
            company_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            file_name: Optional[str] = None,
            file_size: Optional[int] = None,
            content_type: Optional[str] = None,
            token_expiration_hours: int = 24
    ) -> 'UserRegistration':
        """Factory method to create a new user registration"""
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        now = datetime.utcnow()
        verification_token = secrets.token_urlsafe(32)

        return UserRegistration(
            id=id,
            email=email,
            verification_token=verification_token,
            token_expires_at=now + timedelta(hours=token_expiration_hours),
            status=RegistrationStatusEnum.PENDING,
            processing_status=ProcessingStatusEnum.PENDING if file_name else ProcessingStatusEnum.COMPLETED,
            created_at=now,
            updated_at=now,
            company_id=company_id,
            job_position_id=job_position_id,
            existing_user_id=None,
            file_name=file_name,
            file_size=file_size,
            content_type=content_type,
            text_content=None,
            extracted_data=None
        )

    @classmethod
    def _from_repository(
            cls,
            id: UserRegistrationId,
            email: str,
            verification_token: str,
            token_expires_at: datetime,
            status: RegistrationStatusEnum,
            processing_status: ProcessingStatusEnum,
            created_at: datetime,
            updated_at: datetime,
            company_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            existing_user_id: Optional[str] = None,
            file_name: Optional[str] = None,
            file_size: Optional[int] = None,
            content_type: Optional[str] = None,
            text_content: Optional[str] = None,
            extracted_data: Optional[Dict[str, Any]] = None
    ) -> 'UserRegistration':
        """Create UserRegistration from repository data - only for repositories to use"""
        return cls(
            id=id,
            email=email,
            verification_token=verification_token,
            token_expires_at=token_expires_at,
            status=status,
            processing_status=processing_status,
            created_at=created_at,
            updated_at=updated_at,
            company_id=company_id,
            job_position_id=job_position_id,
            existing_user_id=existing_user_id,
            file_name=file_name,
            file_size=file_size,
            content_type=content_type,
            text_content=text_content,
            extracted_data=extracted_data
        )
