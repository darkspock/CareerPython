"""
Page Status Enum - Company page statuses
"""
from enum import Enum


class PageStatus(str, Enum):
    """Possible company page statuses"""
    
    DRAFT = "draft"
    """Draft page, not publicly visible"""
    
    PUBLISHED = "published"
    """Published page, publicly visible"""
    
    ARCHIVED = "archived"
    """Archived page, not publicly visible"""
