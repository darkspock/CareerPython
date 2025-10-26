"""
Talent Pool Status Enum
Phase 8: Enum for talent pool entry status
"""

from enum import Enum


class TalentPoolStatus(str, Enum):
    """Status of a talent pool entry"""

    ACTIVE = "active"  # Actively considering for future positions
    CONTACTED = "contacted"  # Has been contacted for a position
    HIRED = "hired"  # Was hired from the talent pool
    NOT_INTERESTED = "not_interested"  # No longer interested
    ARCHIVED = "archived"  # Archived/removed from active consideration
