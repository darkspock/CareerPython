"""Excepciones del dominio de candidatos"""


class CandidateException(Exception):
    """Excepción base para el dominio de candidatos"""
    pass


class CandidateNotFoundError(CandidateException):
    """Raised when a candidate is not found in the database."""
    pass


class CandidateNotFoundException(CandidateException):
    """Excepción lanzada cuando no se encuentra un candidato"""
    pass


class CandidateAlreadyExistsException(CandidateException):
    """Excepción lanzada cuando se intenta crear un candidato que ya existe"""
    pass


class CandidateValidationException(CandidateException):
    """Excepción lanzada cuando los datos del candidato no son válidos"""
    pass


class CandidateStatusException(CandidateException):
    """Excepción lanzada cuando se intenta una operación no válida con el estado del candidato"""
    pass


class ExperienceNotFoundError(CandidateException):
    """Raised when an experience is not found in the database."""
    pass


class EducationNotFoundError(CandidateException):
    """Raised when an education is not found in the database."""
    pass


class ProjectNotFoundError(CandidateException):
    """Raised when a project is not found in the database."""
    pass
