"""
Subscription and payment-related domain exceptions
"""
from typing import Optional, Any

from .base import BusinessRuleException, ExternalServiceException, ValidationException


class SubscriptionException(BusinessRuleException):
    """Base exception for subscription-related errors"""

    def __init__(
            self,
            message: str,
            subscription_id: Optional[str] = None,
            user_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if subscription_id:
            self.details.update({"subscription_id": subscription_id})
        if user_id:
            self.details.update({"user_id": user_id})


class SubscriptionLimitExceededException(SubscriptionException):
    """Raised when user exceeds subscription limits"""

    def __init__(
            self,
            message: str,
            limit_type: str,
            current_usage: int,
            limit_value: int,
            reset_period: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.limit_type = limit_type
        self.current_usage = current_usage
        self.limit_value = limit_value
        self.reset_period = reset_period
        self.details.update({
            "limit_type": limit_type,
            "current_usage": current_usage,
            "limit_value": limit_value,
            "reset_period": reset_period
        })


class SubscriptionExpiredException(SubscriptionException):
    """Raised when subscription has expired"""

    def __init__(
            self,
            message: str = "Subscription has expired",
            expired_date: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if expired_date:
            self.details.update({"expired_date": expired_date})


class SubscriptionNotActiveException(SubscriptionException):
    """Raised when subscription is not active"""

    def __init__(
            self,
            message: str = "Subscription is not active",
            subscription_status: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if subscription_status:
            self.details.update({"subscription_status": subscription_status})


class InvalidSubscriptionTierException(SubscriptionException):
    """Raised when subscription tier is invalid for operation"""

    def __init__(
            self,
            message: str,
            current_tier: str,
            required_tier: str,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.current_tier = current_tier
        self.required_tier = required_tier
        self.details.update({
            "current_tier": current_tier,
            "required_tier": required_tier
        })


class PaymentException(ExternalServiceException):
    """Base exception for payment-related errors"""

    def __init__(
            self,
            message: str,
            payment_id: Optional[str] = None,
            amount: Optional[float] = None,
            currency: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, service_name="payment_processor", **kwargs)
        if payment_id:
            self.details.update({"payment_id": payment_id})
        if amount:
            self.details.update({"amount": amount})
        if currency:
            self.details.update({"currency": currency})


class PaymentProcessingException(PaymentException):
    """Raised when payment processing fails"""

    def __init__(
            self,
            message: str = "Payment processing failed",
            payment_method: Optional[str] = None,
            decline_reason: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if payment_method:
            self.details.update({"payment_method": payment_method})
        if decline_reason:
            self.details.update({"decline_reason": decline_reason})


class PaymentValidationException(ValidationException):
    """Raised when payment data validation fails"""

    def __init__(
            self,
            message: str,
            validation_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_type:
            self.details.update({"validation_type": validation_type})


class InsufficientFundsException(PaymentException):
    """Raised when payment fails due to insufficient funds"""

    def __init__(
            self,
            message: str = "Insufficient funds for payment",
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)


class PaymentMethodException(PaymentException):
    """Raised when payment method is invalid or expired"""

    def __init__(
            self,
            message: str,
            payment_method_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if payment_method_type:
            self.details.update({"payment_method_type": payment_method_type})


class RefundException(PaymentException):
    """Raised when refund processing fails"""

    def __init__(
            self,
            message: str = "Refund processing failed",
            refund_reason: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if refund_reason:
            self.details.update({"refund_reason": refund_reason})
