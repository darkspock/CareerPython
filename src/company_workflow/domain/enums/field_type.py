from enum import Enum


class FieldType(str, Enum):
    """Types of custom fields that can be added to workflows"""
    TEXT = "TEXT"  # Short text input
    TEXTAREA = "TEXTAREA"  # Long text input
    NUMBER = "NUMBER"  # Numeric input
    CURRENCY = "CURRENCY"  # Currency amount
    DATE = "DATE"  # Date picker
    DROPDOWN = "DROPDOWN"  # Single select dropdown
    MULTI_SELECT = "MULTI_SELECT"  # Multiple select dropdown
    CHECKBOX = "CHECKBOX"  # Boolean checkbox
    RADIO = "RADIO"  # Radio button group
    FILE = "FILE"  # File upload
    URL = "URL"  # URL input
    EMAIL = "EMAIL"  # Email input
    PHONE = "PHONE"  # Phone number input
