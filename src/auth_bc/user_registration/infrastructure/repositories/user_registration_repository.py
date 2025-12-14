from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from src.auth_bc.user_registration.domain.entities import UserRegistration
from src.auth_bc.user_registration.domain.enums import RegistrationStatusEnum, ProcessingStatusEnum
from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId
from src.auth_bc.user_registration.infrastructure.models import UserRegistrationModel


class UserRegistrationRepository(UserRegistrationRepositoryInterface):
    """SQLAlchemy implementation of UserRegistrationRepository"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, registration: UserRegistration) -> None:
        """Save a user registration"""
        model = self._to_model(registration)

        existing = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.id == str(registration.id)
        ).first()

        if existing:
            self._update_model(existing, model)
        else:
            self.session.add(model)

        self.session.commit()

    def get_by_id(self, registration_id: UserRegistrationId) -> Optional[UserRegistration]:
        """Get registration by ID"""
        model = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.id == str(registration_id)
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    def get_by_email(self, email: str) -> Optional[UserRegistration]:
        """Get registration by email (latest pending)"""
        model = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.email == email,
            UserRegistrationModel.status == RegistrationStatusEnum.PENDING
        ).order_by(UserRegistrationModel.created_at.desc()).first()

        if not model:
            return None

        return self._to_entity(model)

    def get_by_verification_token(self, token: str) -> Optional[UserRegistration]:
        """Get registration by verification token"""
        model = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.verification_token == token
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    def get_by_email_and_job_position(
            self, email: str, job_position_id: str
    ) -> Optional[UserRegistration]:
        """Get registration by email and job position"""
        model = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.email == email,
            UserRegistrationModel.job_position_id == job_position_id,
            UserRegistrationModel.status == RegistrationStatusEnum.PENDING
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    def find_expired_registrations(self) -> List[UserRegistration]:
        """Find all expired registrations for cleanup"""
        now = datetime.utcnow()
        models = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.status == RegistrationStatusEnum.PENDING,
            UserRegistrationModel.token_expires_at < now
        ).all()

        return [self._to_entity(m) for m in models]

    def update(self, registration: UserRegistration) -> None:
        """Update an existing registration"""
        existing = self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.id == str(registration.id)
        ).first()

        if not existing:
            raise ValueError(f"Registration {registration.id} not found")

        model = self._to_model(registration)
        self._update_model(existing, model)
        self.session.commit()

    def delete(self, registration_id: UserRegistrationId) -> None:
        """Delete a registration"""
        self.session.query(UserRegistrationModel).filter(
            UserRegistrationModel.id == str(registration_id)
        ).delete()
        self.session.commit()

    # --- Private Methods ---

    def _to_entity(self, model: UserRegistrationModel) -> UserRegistration:
        """Convert SQLAlchemy model to domain entity"""
        return UserRegistration._from_repository(
            id=UserRegistrationId(model.id),
            email=model.email,
            verification_token=model.verification_token,
            token_expires_at=model.token_expires_at,
            status=RegistrationStatusEnum(model.status),
            processing_status=ProcessingStatusEnum(model.processing_status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            company_id=model.company_id,
            job_position_id=model.job_position_id,
            existing_user_id=model.existing_user_id,
            file_name=model.file_name,
            file_size=model.file_size,
            content_type=model.content_type,
            text_content=model.text_content,
            extracted_data=model.extracted_data
        )

    def _to_model(self, entity: UserRegistration) -> UserRegistrationModel:
        """Convert domain entity to SQLAlchemy model"""
        return UserRegistrationModel(
            id=str(entity.id),
            email=entity.email,
            verification_token=entity.verification_token,
            token_expires_at=entity.token_expires_at,
            status=entity.status.value,
            processing_status=entity.processing_status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            company_id=entity.company_id,
            job_position_id=entity.job_position_id,
            existing_user_id=entity.existing_user_id,
            file_name=entity.file_name,
            file_size=entity.file_size,
            content_type=entity.content_type,
            text_content=entity.text_content,
            extracted_data=entity.extracted_data
        )

    def _update_model(self, existing: UserRegistrationModel, new: UserRegistrationModel) -> None:
        """Update existing model with new values"""
        existing.email = new.email
        existing.verification_token = new.verification_token
        existing.token_expires_at = new.token_expires_at
        existing.status = new.status
        existing.processing_status = new.processing_status
        existing.updated_at = new.updated_at
        existing.company_id = new.company_id
        existing.job_position_id = new.job_position_id
        existing.existing_user_id = new.existing_user_id
        existing.file_name = new.file_name
        existing.file_size = new.file_size
        existing.content_type = new.content_type
        existing.text_content = new.text_content
        existing.extracted_data = new.extracted_data
