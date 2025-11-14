from abc import ABC, abstractmethod
from typing import List, Optional

from src.interview_bc.interview_template.domain.entities.interview_template_question import InterviewTemplateQuestion
from src.interview_bc.interview_template.domain.enums import InterviewTemplateQuestionStatusEnum
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview_bc.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId


class InterviewTemplateQuestionRepositoryInterface(ABC):
    """Interface for Interview Template Question Repository"""

    @abstractmethod
    def create(self, interview_template_question: InterviewTemplateQuestion) -> InterviewTemplateQuestion:
        """Create a new question"""
        pass

    @abstractmethod
    def get_by_id(self, id: InterviewTemplateQuestionId) -> Optional[InterviewTemplateQuestion]:
        """Get question by ID"""
        pass

    @abstractmethod
    def get_all(self, interview_template_section_id: Optional[InterviewTemplateSectionId] = None,
                status: Optional[InterviewTemplateQuestionStatusEnum] = None) -> List[InterviewTemplateQuestion]:
        """Get all questions with optional filters"""
        pass

    @abstractmethod
    def update(self, question: InterviewTemplateQuestion) -> None:
        """Update question - same pattern as InterviewTemplateRepository"""
        pass

    @abstractmethod
    def delete(self, interview_template_question_id: InterviewTemplateQuestionId) -> bool:
        """Delete question by ID"""
        pass

    @abstractmethod
    def get_by_section_id(self, section_id: InterviewTemplateSectionId) -> List[InterviewTemplateQuestion]:
        """Get all questions for a specific section"""
        pass

    @abstractmethod
    def update_entity(self, question: InterviewTemplateQuestion) -> None:
        """Update a question entity (for use with command handlers)"""
        pass
