from abc import ABC, abstractmethod
from typing import List, Optional, Any

from src.interview.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview.interview_template.domain.enums import InterviewTemplateTypeEnum
from src.interview.interview_template.domain.value_objects import InterviewTemplateId
from src.shared.domain.enums.job_category import JobCategoryEnum


class InterviewTemplateRepositoryInterface(ABC):
    """Interface for Interview Template Repository with all available methods"""

    # Basic CRUD Operations

    @abstractmethod
    def create(self, template: InterviewTemplate) -> InterviewTemplate:
        """Create a new template"""
        pass

    @abstractmethod
    def get_by_id(self, template_id: InterviewTemplateId) -> Optional[InterviewTemplate]:
        """Get template by ID"""
        pass

    @abstractmethod
    def update(self, template: InterviewTemplate) -> None:
        """Update existing template"""
        pass

    @abstractmethod
    def delete(self, template_id: str, soft_delete: bool = True) -> bool:
        """Delete template (soft delete by default)"""
        pass

    # Search and Filtering

    @abstractmethod
    def search(self, **criteria: Any) -> List[InterviewTemplate]:
        """Advanced template search with multiple criteria"""
        pass

    @abstractmethod
    def get_by_type(self, template_type: InterviewTemplateTypeEnum, include_disabled: bool = False) -> List[InterviewTemplate]:
        """Get templates by type"""
        pass

    @abstractmethod
    def get_by_job_category(self, job_category: Optional[JobCategoryEnum]) -> List[InterviewTemplate]:
        """Get templates by job category"""
        pass

    # Utility Methods

    @abstractmethod
    def clone_template(self, template_id: str, new_name: str, created_by: Optional[str] = None) -> InterviewTemplate:
        """Clone existing template with new ID"""
        pass
