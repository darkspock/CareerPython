from abc import ABC, abstractmethod
from typing import List, Optional

from src.interview.interview_template.domain.entities.interview_template_section import InterviewTemplateSection
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId


class InterviewTemplateSectionRepositoryInterface(ABC):
    """Interface for Interview Template Section Repository"""

    @abstractmethod
    def create(self, section: InterviewTemplateSection) -> InterviewTemplateSection:
        """Create a new section"""
        pass

    @abstractmethod
    def get_by_id(self, section_id: InterviewTemplateSectionId) -> Optional[InterviewTemplateSection]:
        """Get section by ID"""
        pass

    @abstractmethod
    def get_by_template_id(self, template_id: InterviewTemplateId) -> List[InterviewTemplateSection]:
        """Get all sections for a template"""
        pass

    @abstractmethod
    def update(self, section: InterviewTemplateSection) -> InterviewTemplateSection:
        """Update an existing section"""
        pass

    @abstractmethod
    def delete(self, section_id: InterviewTemplateSectionId) -> bool:
        """Delete a section"""
        pass
