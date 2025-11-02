from enum import Enum


class CompanyUserInvitationStatus(str, Enum):
    """Status of a company user invitation"""
    PENDING = "pending"  # Invitación pendiente
    ACCEPTED = "accepted"  # Invitación aceptada
    REJECTED = "rejected"  # Invitación rechazada
    EXPIRED = "expired"  # Invitación expirada
    CANCELLED = "cancelled"  # Invitación cancelada

