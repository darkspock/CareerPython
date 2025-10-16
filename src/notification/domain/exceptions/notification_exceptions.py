class NotificationException(Exception):
    """Excepción base para notificaciones"""
    pass


class EmailSendingException(NotificationException):
    """Excepción para errores al enviar emails"""
    pass


class TemplateNotFoundException(NotificationException):
    """Excepción cuando no se encuentra un template"""
    pass


class InvalidEmailAddressException(NotificationException):
    """Excepción para direcciones de email inválidas"""
    pass
