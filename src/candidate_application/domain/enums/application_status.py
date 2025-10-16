from enum import Enum


class ApplicationStatusEnum(str, Enum):
    """Estados de la aplicación de candidato"""
    APPLIED = "applied"
    REVIEWING = "reviewing"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"
