from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.notification_bc.in_app_notification.domain.entities.in_app_notification import (
    InAppNotification,
    InAppNotificationId
)
from src.notification_bc.in_app_notification.domain.enums.notification_enums import (
    InAppNotificationType,
    InAppNotificationPriority
)
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)
from src.notification_bc.in_app_notification.infrastructure.models.in_app_notification_model import (
    InAppNotificationModel
)


class InAppNotificationRepository(InAppNotificationRepositoryInterface):
    """SQLAlchemy implementation of InAppNotificationRepository"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, notification_id: InAppNotificationId) -> Optional[InAppNotification]:
        model = self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.id == str(notification_id.value)
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    def list_by_user(
        self,
        user_id: str,
        company_id: str,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False
    ) -> Tuple[List[InAppNotification], int]:
        query = self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.user_id == user_id,
            InAppNotificationModel.company_id == company_id
        )

        if unread_only:
            query = query.filter(InAppNotificationModel.is_read == False)

        # Get total count
        total_count = query.count()

        # Get paginated results, ordered by creation date descending
        models = query.order_by(
            InAppNotificationModel.created_at.desc()
        ).offset(offset).limit(limit).all()

        return [self._to_entity(m) for m in models], total_count

    def get_unread_count(self, user_id: str, company_id: str) -> int:
        return self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.user_id == user_id,
            InAppNotificationModel.company_id == company_id,
            InAppNotificationModel.is_read == False
        ).count()

    def save(self, notification: InAppNotification) -> None:
        model = self._to_model(notification)

        existing = self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.id == str(notification.id.value)
        ).first()

        if existing:
            # Update existing
            existing.is_read = model.is_read
            existing.read_at = model.read_at
        else:
            # Insert new
            self.session.add(model)

        self.session.commit()

    def mark_as_read(self, notification_id: InAppNotificationId) -> None:
        self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.id == str(notification_id.value)
        ).update({
            InAppNotificationModel.is_read: True,
            InAppNotificationModel.read_at: datetime.utcnow()
        })
        self.session.commit()

    def mark_all_as_read(self, user_id: str, company_id: str) -> int:
        result = self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.user_id == user_id,
            InAppNotificationModel.company_id == company_id,
            InAppNotificationModel.is_read == False
        ).update({
            InAppNotificationModel.is_read: True,
            InAppNotificationModel.read_at: datetime.utcnow()
        })
        self.session.commit()
        return result

    def delete(self, notification_id: InAppNotificationId) -> None:
        self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.id == str(notification_id.value)
        ).delete()
        self.session.commit()

    def delete_old_notifications(self, user_id: str, company_id: str, days: int = 30) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = self.session.query(InAppNotificationModel).filter(
            InAppNotificationModel.user_id == user_id,
            InAppNotificationModel.company_id == company_id,
            InAppNotificationModel.created_at < cutoff_date
        ).delete()
        self.session.commit()
        return result

    def _to_entity(self, model: InAppNotificationModel) -> InAppNotification:
        """Convert SQLAlchemy model to domain entity"""
        # Cast to handle SQLAlchemy's Optional type hints
        # Non-nullable columns in the DB will always have values
        return InAppNotification(
            id=InAppNotificationId(str(model.id)),
            user_id=str(model.user_id),
            company_id=str(model.company_id),
            notification_type=InAppNotificationType(str(model.notification_type)),
            title=str(model.title),
            message=str(model.message),
            priority=InAppNotificationPriority(str(model.priority)),
            is_read=bool(model.is_read),
            created_at=model.created_at,  # type: ignore[arg-type]
            read_at=model.read_at,
            link=model.link,
            metadata=model.notification_metadata
        )

    def _to_model(self, entity: InAppNotification) -> InAppNotificationModel:
        """Convert domain entity to SQLAlchemy model"""
        return InAppNotificationModel(
            id=str(entity.id.value),
            user_id=entity.user_id,
            company_id=entity.company_id,
            notification_type=entity.notification_type.value,
            title=entity.title,
            message=entity.message,
            priority=entity.priority.value,
            is_read=entity.is_read,
            created_at=entity.created_at,
            read_at=entity.read_at,
            link=entity.link,
            notification_metadata=entity.metadata
        )
