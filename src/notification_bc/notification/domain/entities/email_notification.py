from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.framework.domain.value_objects.base_id import BaseId
from src.notification_bc.notification.domain.enums.notification_type import NotificationTypeEnum, NotificationStatusEnum


@dataclass(frozen=True)
class NotificationId(BaseId):
    pass


@dataclass
class EmailNotification:
    """Entidad del dominio para notificaciones por email"""
    id: NotificationId
    recipient_email: str
    subject: str
    template_name: str
    notification_type: NotificationTypeEnum
    status: NotificationStatusEnum
    template_data: Dict[str, Any]
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None

    def mark_as_sent(self) -> None:
        """Marcar como enviado"""
        self.status = NotificationStatusEnum.SENT
        self.sent_at = datetime.utcnow()

    def mark_as_delivered(self) -> None:
        """Marcar como entregado"""
        self.status = NotificationStatusEnum.DELIVERED
        self.delivered_at = datetime.utcnow()

    def mark_as_failed(self, error_message: str) -> None:
        """Marcar como fallido"""
        self.status = NotificationStatusEnum.FAILED
        self.error_message = error_message

    @staticmethod
    def create(
            id: NotificationId,
            recipient_email: str,
            subject: str,
            template_name: str,
            notification_type: NotificationTypeEnum,
            template_data: Dict[str, Any]
    ) -> 'EmailNotification':
        """Factory method para crear una nueva notificación"""
        return EmailNotification(
            id=id,
            recipient_email=recipient_email,
            subject=subject,
            template_name=template_name,
            notification_type=notification_type,
            status=NotificationStatusEnum.PENDING,
            template_data=template_data,
            created_at=datetime.utcnow(),
            sent_at=None,
            delivered_at=None,
            error_message=None
        )
