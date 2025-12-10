import enum


class ClosedReasonEnum(str, enum.Enum):
    """Reason for closing a job position"""
    FILLED = "filled"           # Position was filled (hired someone)
    CANCELLED = "cancelled"     # Position no longer needed
    BUDGET_CUT = "budget_cut"   # Budget constraints
    DUPLICATE = "duplicate"     # Duplicate of another position
    OTHER = "other"             # Other reason (requires note)
