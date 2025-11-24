"""
Request schemas for stage style operations
"""
from typing import Optional

from pydantic import BaseModel, Field, validator


class UpdateStageStyleRequest(BaseModel):
    """Request schema for updating stage style"""

    icon: Optional[str] = Field(None, description="Stage icon (emoji, HTML icon, or SVG)")
    color: Optional[str] = Field(None, description="Text color (hex, rgb, or CSS color name)")
    background_color: Optional[str] = Field(None, description="Background color (hex, rgb, or CSS color name)")

    @validator('icon')
    def validate_icon(cls, v: Optional[str]) -> Optional[str]:
        """Validate icon format"""
        if v is not None:
            if not v.strip():
                raise ValueError("Icon cannot be empty")
            if len(v) > 1000:
                raise ValueError("Icon cannot exceed 1000 characters")
            if v.startswith('<') and not v.endswith('>'):
                raise ValueError("Invalid HTML icon format")
        return v

    @validator('color')
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate color format"""
        if v is not None:
            if not v.strip():
                raise ValueError("Color cannot be empty")

            # Basic color validation - in production, use a more robust validator
            import re
            hex_pattern = r'^#[0-9A-Fa-f]{6}$'
            rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
            rgba_pattern = r'^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$'

            css_colors = {
                'black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
                'pink', 'brown', 'gray', 'grey', 'transparent', 'currentColor'
            }

            if not (
                    re.match(hex_pattern, v) or
                    re.match(rgb_pattern, v) or
                    re.match(rgba_pattern, v) or
                    v.lower() in css_colors
            ):
                raise ValueError(f"Invalid color format: {v}")
        return v

    @validator('background_color')
    def validate_background_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate background color format"""
        if v is not None:
            if not v.strip():
                raise ValueError("Background color cannot be empty")

            # Basic color validation - in production, use a more robust validator
            import re
            hex_pattern = r'^#[0-9A-Fa-f]{6}$'
            rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
            rgba_pattern = r'^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$'

            css_colors = {
                'black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
                'pink', 'brown', 'gray', 'grey', 'transparent', 'currentColor'
            }

            if not (
                    re.match(hex_pattern, v) or
                    re.match(rgb_pattern, v) or
                    re.match(rgba_pattern, v) or
                    v.lower() in css_colors
            ):
                raise ValueError(f"Invalid background color format: {v}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "icon": "✅",
                "color": "#065f46",
                "background_color": "#d1fae5"
            }
        }
