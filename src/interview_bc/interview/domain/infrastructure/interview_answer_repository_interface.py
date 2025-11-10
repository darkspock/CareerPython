"""Interview Answer repository interface"""
from abc import ABC, abstractmethod
from typing import Optional, List

from src.interview_bc.interview.domain.entities.interview_answer import InterviewAnswer
from src.interview_bc.interview.domain.value_objects.interview_answer_id import InterviewAnswerId


class InterviewAnswerRepositoryInterface(ABC):
    """Interface for Interview Answer repository"""

    @abstractmethod
    def create(self, interview_answer: InterviewAnswer) -> InterviewAnswer:
        """Create a new interview answer"""
        pass

    @abstractmethod
    def get_by_id(self, answer_id: str) -> Optional[InterviewAnswer]:
        """Get interview answer by ID"""
        pass

    @abstractmethod
    def update(self, interview_answer: InterviewAnswer) -> InterviewAnswer:
        """Update an existing interview answer"""
        pass

    @abstractmethod
    def delete(self, id: InterviewAnswerId) -> bool:
        """Delete an interview answer"""
        pass

    @abstractmethod
    def get_by_interview_id(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all answers for an interview"""
        pass

    @abstractmethod
    def get_by_question_id(self, question_id: str) -> List[InterviewAnswer]:
        """Get all answers for a specific question"""
        pass

    @abstractmethod
    def get_by_interview_and_question(self, interview_id: str, question_id: str) -> Optional[InterviewAnswer]:
        """Get answer for specific interview and question"""
        pass

    @abstractmethod
    def get_scored_answers_by_interview(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all scored answers for an interview"""
        pass

    @abstractmethod
    def get_unscored_answers_by_interview(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all unscored answers for an interview"""
        pass

    @abstractmethod
    def count_by_interview(self, interview_id: str) -> int:
        """Count answers for an interview"""
        pass

    @abstractmethod
    def count_scored_by_interview(self, interview_id: str) -> int:
        """Count scored answers for an interview"""
        pass

    @abstractmethod
    def get_average_score_by_interview(self, interview_id: str) -> Optional[float]:
        """Get average score for an interview"""
        pass
