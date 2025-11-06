import logging
from typing import Optional, List

from core.database import DatabaseInterface
from src.company.domain.entities.company_user_invitation import CompanyUserInvitation
from src.company.domain.enums import CompanyUserInvitationStatus
from src.company.domain.infrastructure.company_user_invitation_repository_interface import (
    CompanyUserInvitationRepositoryInterface
)
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company.domain.value_objects.company_user_invitation_id import CompanyUserInvitationId
from src.company.domain.value_objects.invitation_token import InvitationToken
from src.company.infrastructure.models.company_user_invitation_model import CompanyUserInvitationModel

logger = logging.getLogger(__name__)


class CompanyUserInvitationRepository(CompanyUserInvitationRepositoryInterface):
    """Company user invitation repository implementation"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, invitation: CompanyUserInvitation) -> None:
        """Save or update a company user invitation"""
        try:
            model = self._to_model(invitation)
            with self.database.get_session() as session:
                session.merge(model)
                session.commit()
                logger.info(f"Saved invitation {invitation.id} for email {invitation.email}")
        except Exception as e:
            logger.error(f"Error saving invitation {invitation.id}: {str(e)}", exc_info=True)
            raise

    def get_by_id(self, invitation_id: CompanyUserInvitationId) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyUserInvitationModel).filter(
                CompanyUserInvitationModel.id == str(invitation_id)
            ).first()
            return self._to_domain(model) if model else None

    def get_by_token(self, token: InvitationToken) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by token"""
        try:
            with self.database.get_session() as session:
                model = session.query(CompanyUserInvitationModel).filter(
                    CompanyUserInvitationModel.token == str(token)
                ).first()
                if model:
                    logger.debug(f"Found invitation by token for email {model.email}")
                return self._to_domain(model) if model else None
        except Exception as e:
            logger.error(f"Error getting invitation by token: {str(e)}", exc_info=True)
            raise

    def get_by_email_and_company(
            self,
            email: str,
            company_id: CompanyId
    ) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by email and company ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyUserInvitationModel).filter(
                CompanyUserInvitationModel.email == email.lower(),
                CompanyUserInvitationModel.company_id == str(company_id)
            ).first()
            return self._to_domain(model) if model else None

    def find_pending_by_email(self, email: str) -> List[CompanyUserInvitation]:
        """Find all pending invitations for an email"""
        with self.database.get_session() as session:
            models = session.query(CompanyUserInvitationModel).filter(
                CompanyUserInvitationModel.email == email.lower(),
                CompanyUserInvitationModel.status == CompanyUserInvitationStatus.PENDING.value
            ).all()
            return [self._to_domain(m) for m in models]

    def find_expired(self) -> List[CompanyUserInvitation]:
        """Find all expired invitations"""
        from datetime import datetime
        with self.database.get_session() as session:
            models = session.query(CompanyUserInvitationModel).filter(
                CompanyUserInvitationModel.expires_at < datetime.utcnow(),
                CompanyUserInvitationModel.status == CompanyUserInvitationStatus.PENDING.value
            ).all()
            return [self._to_domain(m) for m in models]

    def delete(self, invitation_id: CompanyUserInvitationId) -> None:
        """Delete a company user invitation"""
        try:
            with self.database.get_session() as session:
                deleted_count = session.query(CompanyUserInvitationModel).filter(
                    CompanyUserInvitationModel.id == str(invitation_id)
                ).delete()
                session.commit()
                if deleted_count > 0:
                    logger.info(f"Deleted invitation {invitation_id}")
                else:
                    logger.warning(f"Attempted to delete non-existent invitation {invitation_id}")
        except Exception as e:
            logger.error(f"Error deleting invitation {invitation_id}: {str(e)}", exc_info=True)
            raise

    def _to_domain(self, model: CompanyUserInvitationModel) -> CompanyUserInvitation:
        """Convert model to domain entity"""
        return CompanyUserInvitation(
            id=CompanyUserInvitationId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            email=model.email,
            invited_by_user_id=CompanyUserId.from_string(model.invited_by_user_id),
            token=InvitationToken.from_string(model.token),
            status=CompanyUserInvitationStatus(model.status),
            expires_at=model.expires_at,
            accepted_at=model.accepted_at,
            rejected_at=model.rejected_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CompanyUserInvitation) -> CompanyUserInvitationModel:
        """Convert domain entity to model"""
        return CompanyUserInvitationModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            email=entity.email,
            invited_by_user_id=str(entity.invited_by_user_id),
            token=str(entity.token),
            status=entity.status.value,
            expires_at=entity.expires_at,
            accepted_at=entity.accepted_at,
            rejected_at=entity.rejected_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
