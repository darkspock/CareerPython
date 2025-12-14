from abc import ABC, abstractmethod
from typing import Optional, List

from src.auth_bc.user_registration.domain.entities import UserRegistration
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId


class UserRegistrationRepositoryInterface(ABC):
    """Repository interface for UserRegistration entity"""

    @abstractmethod
    def save(self, registration: UserRegistration) -> None:
        """Save a user registration"""
        pass

    @abstractmethod
    def get_by_id(self, registration_id: UserRegistrationId) -> Optional[UserRegistration]:
        """Get registration by ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserRegistration]:
        """Get registration by email (latest pending)"""
        pass

    @abstractmethod
    def get_by_verification_token(self, token: str) -> Optional[UserRegistration]:
        """Get registration by verification token"""
        pass

    @abstractmethod
    def get_by_email_and_job_position(
            self, email: str, job_position_id: str
    ) -> Optional[UserRegistration]:
        """Get registration by email and job position"""
        pass

    @abstractmethod
    def find_expired_registrations(self) -> List[UserRegistration]:
        """Find all expired registrations for cleanup"""
        pass

    @abstractmethod
    def update(self, registration: UserRegistration) -> None:
        """Update an existing registration"""
        pass

    @abstractmethod
    def delete(self, registration_id: UserRegistrationId) -> None:
        """Delete a registration"""
        pass
