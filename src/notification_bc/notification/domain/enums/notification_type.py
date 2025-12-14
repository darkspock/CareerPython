from enum import Enum


class NotificationTypeEnum(str, Enum):
    """Tipos de notificaciones"""
    WELCOME_EMAIL = "welcome_email"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_ACTIVATION = "account_activation"
    EMAIL_VERIFICATION = "email_verification"
    APPLICATION_CONFIRMATION = "application_confirmation"
    INTERVIEW_INVITATION = "interview_invitation"
    SUBSCRIPTION_CONFIRMATION = "subscription_confirmation"
    SUBSCRIPTION_RENEWAL_REMINDER = "subscription_renewal_reminder"
    SUBSCRIPTION_EXPIRED = "subscription_expired"


class NotificationStatusEnum(str, Enum):
    """Estados de las notificaciones"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
