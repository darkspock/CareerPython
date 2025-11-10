"""Job position visibility enum"""
import enum


class JobPositionVisibilityEnum(str, enum.Enum):
    """Visibility levels for job positions"""
    HIDDEN = "hidden"  # Solo visible internamente
    INTERNAL = "internal"  # Visible para usuarios de la empresa
    PUBLIC = "public"  # Visible para candidatos (público)

