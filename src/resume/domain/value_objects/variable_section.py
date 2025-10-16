import re
from dataclasses import dataclass
from typing import List


@dataclass
class VariableSection:
    """Value Object for variable resume sections with HTML content"""
    key: str
    title: str
    content: str = ""  # HTML content
    order: int = 0

    def __post_init__(self) -> None:
        """Validate section data"""
        if not self.key:
            raise ValueError("Section key cannot be empty")

        if not self.title:
            raise ValueError("Section title cannot be empty")

        # Validate key format (lowercase, underscore, no spaces)
        if not re.match(r'^[a-z][a-z0-9_]*$', self.key):
            raise ValueError("Section key must be lowercase with underscores only")

        # Basic HTML sanitization - remove dangerous tags
        if self.content:
            self.content = self._sanitize_html(self.content)

    def _sanitize_html(self, html_content: str) -> str:
        """Basic HTML sanitization - remove dangerous tags"""
        # Remove script tags and their content
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Remove style tags and their content
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # Remove on* event attributes (onclick, onload, etc.)
        html_content = re.sub(r'\son\w+\s*=\s*["\'][^"\']*["\']', '', html_content, flags=re.IGNORECASE)

        # Remove javascript: urls
        html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)

        return html_content

    def is_empty(self) -> bool:
        """Check if section content is empty"""
        # Remove HTML tags for checking
        text_content = re.sub(r'<[^>]+>', '', self.content).strip()
        return not bool(text_content)

    def get_text_content(self) -> str:
        """Extract plain text from HTML content"""
        return re.sub(r'<[^>]+>', '', self.content).strip()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'key': self.key,
            'title': self.title,
            'content': self.content,
            'order': self.order
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'VariableSection':
        """Create from dictionary"""
        return cls(
            key=data.get('key', ''),
            title=data.get('title', ''),
            content=data.get('content', ''),
            order=data.get('order', 0)
        )

    @classmethod
    def create_default_sections(cls) -> List['VariableSection']:
        """Create default variable sections"""
        return [
            cls(key='summary', title='Professional Summary', order=1),
            cls(key='experience', title='Work Experience', order=2),
            cls(key='education', title='Education', order=3),
            cls(key='skills', title='Skills', order=4),
            cls(key='projects', title='Projects', order=5)
        ]
