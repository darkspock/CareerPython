"""Core domain exceptions module.

This module contains the base exception classes and specific domain exceptions
used throughout the application for error handling and business rule validation.
"""

"""Core domain exceptions module.

This module contains the base exception classes and common domain exceptions
used throughout the application for consistent error handling.
"""

from typing import Optional

"""Core domain exceptions module.

This module contains the base exception classes and common domain exceptions
used throughout the application for consistent error handling.
"""


class DomainException(Exception):
    """Excepción base para errores del dominio"""
    pass


class EntityNotFoundException(DomainException):
    """Excepción cuando no se encuentra una entidad"""
    
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class ValidationException(DomainException):
    """Excepción para errores de validación"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


class BusinessRuleException(DomainException):
    """Excepción para violaciones de reglas de negocio"""
    pass


class AuthenticationException(DomainException):
    """Excepción para errores de autenticación"""
    pass


class AuthorizationException(DomainException):
    """Excepción para errores de autorización"""
    pass


class UserAlreadyExistsException(DomainException):
    """Excepción cuando un usuario ya existe"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists") 