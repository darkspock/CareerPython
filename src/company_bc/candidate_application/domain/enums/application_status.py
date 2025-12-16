from enum import Enum


class ApplicationStatusEnum(str, Enum):
    """Estados de la aplicación de candidato"""
    # Phase 8: New states for CV builder flow
    DRAFT = "draft"  # Started but not submitted
    PENDING_CV = "pending_cv"  # Waiting for CV generation (CV builder flow)
    # Standard application states
    APPLIED = "applied"
    REVIEWING = "reviewing"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"
